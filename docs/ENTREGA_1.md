# ENTREGA 1: Backend Completo + Frontend Base

## Objetivo de la Entrega
Backend funcional con API REST, WebSocket, autenticación JWT y base de datos SQLite. Frontend con conexión WebSocket y login funcional.

## Dependencias Previas (ya implementadas)
- `backend/core/` (traffic_light, vehicle, scheduler, intersection)
- `backend/simulation/` (engine, network)

---

## Tarea 1: `backend/config.py` — Configuración Global

**Archivo a crear:** `backend/config.py`

**Descripción:**
Crear archivo de configuración centralizado para todo el proyecto.

**Contenido esperado:**
```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = os.getenv("DB_PATH", str(BASE_DIR / "traffic.db"))

JWT_SECRET = os.getenv("JWT_SECRET", "traffic-system-secret")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 8

SIMULATION_TICK_INTERVAL = 1.0  # segundos entre ticks del kernel
FAULT_MIN_INTERVAL = 15  # segundos mínimos entre fallos
FAULT_MAX_INTERVAL = 30  # segundos máximos entre fallos
FAULT_RECOVERY_TIME = 5  # segundos hasta auto-recuperación

TRAFFIC_LIGHT_DEFAULT_GREEN = 10
TRAFFIC_LIGHT_DEFAULT_RED = 10
TRAFFIC_LIGHT_YELLOW_DURATION = 3

API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
```

**Notas:**
- Usar `pydantic.BaseModel` para validación de settings
- Exportar instancia única como `settings`

---

## Tarea 2: `backend/main.py` — Entry Point FastAPI

**Archivo a crear:** `backend/main.py`

**Descripción:**
Punto de entrada FastAPI con lifespan, CORS, inclusión de routers y conexión a la base de datos.

**Endpoints a incluir:**
- Rutas de auth desde `api.routes_auth`
- Rutas de simulación desde `api.routes_simulation`
- Rutas de control desde `api.routes_control`
- WebSocket en `/ws`
- Documentación OpenAPI en `/docs`

**Estructura esperada:**
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes_auth import router as auth_router
from api.routes_simulation import router as simulation_router
from api.routes_control import router as control_router
from api.websocket import manager
from db.database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: crear tablas
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: cleanup si necesario

app = FastAPI(title="Traffic System API", lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(auth_router)
app.include_router(simulation_router)
app.include_router(control_router)
app.include_router(websocket_router)  # definir en websocket.py

@app.get("/")
def root():
    return {"status": "running", "system": "Traffic Management"}
```

**Notas:**
- Integrar `SimulationEngine` para que `/simulation/start` lo instancie
- El `manager` de websocket debe ser accesible globalmente o vía dependency injection
- Usar `on_event("startup")` y `on_event("shutdown")` si lifespan no está disponible en la versión de FastAPI usada

---

## Tarea 3: `backend/auth/jwt_handler.py` — Manejo de Tokens JWT

**Archivo a crear:** `backend/auth/jwt_handler.py`

**Descripción:**
Módulo para crear y validar tokens JWT, con autenticación via OAuth2PasswordBearer.

**Funcionalidades requeridas:**
1. `create_token(user_id: str, role: str) -> str`
   - Payload: `sub` (user_id), `role`, `exp` (8 horas)
   - Codificar con HS256

2. `decode_token(token: str) -> dict`
   - Decodificar y retornar payload
   - Lanzar `JWTError` si expira o es inválido

3. `oauth2_scheme` - instancia OAuth2PasswordBearer(tokenUrl="/auth/login")

4. `get_current_user(token: str = Depends(oauth2_scheme)) -> dict`
   - Dependencia FastAPI para obtener usuario del token

**Dependencias:**
```python
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
```

**Constantes (usar de config.py):**
```python
SECRET_KEY = "traffic-system-secret"  # importar de config
ALGORITHM = "HS256"
```

---

## Tarea 4: `backend/auth/roles.py` — Decoradores de Autorización

**Archivo a crear:** `backend/auth/roles.py`

**Descripción:**
Decoradores de dependencia FastAPI para proteger rutas por rol.

**Funcionalidades requeridas:**

1. `ROLES = ["viewer", "control"]` - lista de roles válidos

2. `require_role(required_role: str)`
   - Decorador que crea una dependencia FastAPI
   - Verifica que `payload.get("role") == required_role`
   - Retorna 403 si rol insuficiente
   - Retorna 401 si token inválido

3. `require_any_role(*roles)` - alternativo que acepta cualquiera de los roles dados

4. `get_optional_user()` - dependencia que retorna usuario sin requerir auth (None si no hay token)

**Ejemplo de uso:**
```python
@router.put("/lights/{id}/timing")
def update_timing(id: str, user=Depends(require_role("control"))):
    # user["sub"] = user_id
    # user["role"] = role
    ...
```

---

## Tarea 5: `backend/api/routes_auth.py` — Rutas de Autenticación

**Archivo a crear:** `backend/api/routes_auth.py`

**Descripción:**
Rutas REST para login y registro de usuarios.

**Endpoints:**

### `POST /auth/register`
- Body: `{"username": str, "password": str, "role": "viewer"|"control"}`
- Validar username único
- Hashear password con bcrypt
- Guardar en tabla `users`
- Retornar `{"message": "User created", "user_id": str}`

### `POST /auth/login`
- Body: form data (OAuth2PasswordRequestForm) con `username` y `password`
- Verificar credentials contra bcrypt
- Retornar `{"access_token": str, "token_type": "bearer", "role": str}`

**Dependencias:**
```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from db.database import get_db
from db.models import User
from auth.jwt_handler import create_token
```

**Notas:**
- Usar `bcrypt` via `passlib.context.CryptContext(scheme="bcrypt")`
- La tabla users ya debe existir (creada en startup de main.py)

---

## Tarea 6: `backend/api/websocket.py` — WebSocket Broadcast

**Archivo a crear:** `backend/api/websocket.py`

**Descripción:**
Gestor de conexiones WebSocket y broadcast de estado en tiempo real.

**Clase `ConnectionManager`:**
```python
class ConnectionManager:
    def __init__(self):
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    async def disconnect(self, ws: WebSocket):
        if ws in self.active:
            self.active.remove(ws)

    async def broadcast(self, data: dict):
        """Envía a todos los clientes conectados."""
        import json
        msg = json.dumps(data)
        for ws in self.active:
            try:
                await ws.send_text(msg)
            except:
                await self.disconnect(ws)
```

**Router WebSocket:**
```python
@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    manager.connect(ws)
    try:
        while True:
            # Receive messages from client (keep-alive, ping, etc)
            data = await ws.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(ws)
```

**Formato de mensajes broadcast:**
```python
{
    "type": "STATE_UPDATE",  # | "FAULT" | "EMERGENCY" | "VEHICLE_DONE"
    "intersections": [...],   # lista de estados de intersecciones
    "vehicles": [...],        # lista de estados de vehículos
    "alerts": [...],         # alertas activas
    "timestamp": "ISO8601"
}
```

**Variable global:**
```python
manager = ConnectionManager()
```

**Integración con SimulationEngine:**
- El engine debe tener referencia a `manager` para llamar `await manager.broadcast(state)` en cada tick
- Verificar cómo pasar el manager al engine (sugerencia: en `main.py` crear engine después de importar manager)

---

## Tarea 7: `backend/api/routes_simulation.py` — Rutas de Simulación

**Archivo a crear:** `backend/api/routes_simulation.py`

**Descripción:**
Rutas para controlar la simulación: start, stop, status, y agregar vehículos.

**Endpoints:**

### `POST /simulation/start`
- **Rol requerido:** `control`
- Sin body
- Crear instancia de `SimulationEngine` (importado de simulation.engine)
- Crear red de intersecciones (usar `TrafficNetwork` de network.py)
- Iniciar FaultHandler
- Retornar `{"status": "started", "intersections": N}`

### `POST /simulation/stop`
- **Rol requerido:** `control`
- Detener engine y fault handler
- Retornar `{"status": "stopped"}`

### `GET /simulation/status`
- **Rol requerido:** `viewer` (o `control`)
- Retornar estado actual:
```python
{
    "running": bool,
    "tick": int,
    "intersections": [
        {
            "id": str,
            "state": "RED"|"GREEN"|"YELLOW"|"FAULT",
            "position": {"x": int, "y": int},
            "vehicle_count": int
        }
    ],
    "vehicles": [
        {
            "id": str,
            "status": "WAITING"|"MOVING"|"DONE"|"BLOCKED",
            "position": int,  # índice en ruta
            "route": [str],    # ids de intersecciones
            "priority": "EMERGENCY"|"HIGH"|"NORMAL"
        }
    ]
}
```

### `POST /simulation/vehicle`
- **Rol requerido:** `control`
- Body: `{"id": str, "route": [str], "priority": "EMERGENCY"|"HIGH"|"NORMAL"}`
- Agregar vehículo a la simulación (llamar método del engine)
- Retornar `{"status": "vehicle_added", "vehicle_id": str}`

**Notas:**
- Mantener referencia global al engine en `main.py` o como variable de aplicación
- Para compartir estado entre routes y websocket, el engine debe tener método `get_snapshot()` que retorne el formato de arriba

---

## Tarea 8: `backend/api/routes_control.py` — Rutas de Control de Semáforos

**Archivo a crear:** `backend/api/routes_control.py`

**Descripción:**
Rutas para modificar configuración de semáforos y simular fallos manualmente.

**Endpoints:**

### `PUT /control/lights/{intersection_id}/timing`
- **Rol requerido:** `control`
- Body: `{"green_time": int, "red_time": int}`
- Actualizar tiempos del semáforo en la intersección
- Guardar cambio en `light_config` de la DB
- Retornar `{"status": "updated", "intersection": id, "green_time": int, "red_time": int}`

### `POST /control/lights/{intersection_id}/fault`
- **Rol requerido:** `control`
- Trigger fault manual en el semáforo indicado
- Retornar `{"status": "fault_triggered", "intersection": id}`

### `GET /control/lights`
- **Rol requerido:** `control`
- Listar configuración de todos los semáforos
- Retornar lista de configs con tiempos actuales

### `GET /logs`
- **Rol requerido:** `control`
- Query params opcionales: `?event_type=FAULT&limit=100`
- Retornar últimos eventos del event_log

**Notas:**
- Usar `auth.roles.require_role` como dependencia
- Llamar métodos del engine para aplicar cambios en tiempo real
- Registrar cambios de config en `event_log` con `event_type="CONFIG_CHANGE"`

---

## Tarea 9: `backend/db/database.py` — Conexión SQLite

**Archivo a crear:** `backend/db/database.py`

**Descripción:**
Configuración de la conexión SQLite con SQLAlchemy.

**Contenido:**
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DB_PATH

engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency para obtener sesión de DB en rutas FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Notas:**
- `check_same_thread=False` necesario porque FastAPI usa múltiples threads
- Exportar `Base` para que models.py lo use

---

## Tarea 10: `backend/db/models.py` — Modelos SQLAlchemy

**Archivo a crear:** `backend/db/models.py`

**Descripción:**
Modelos de base de datos para Users, EventLog y LightConfig.

**Modelos:**

### `User`
```python
class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "viewer" o "control"
```

### `EventLog`
```python
class EventLog(Base):
    __tablename__ = "event_log"
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(String, nullable=False)
    event_type = Column(String, nullable=False)  # FAULT | EMERGENCY | CONFIG_CHANGE | DEADLOCK
    intersection_id = Column(String, nullable=True)
    vehicle_id = Column(String, nullable=True)
    details = Column(Text, nullable=True)  # JSON string
    user_id = Column(String, nullable=True)
```

### `LightConfig`
```python
class LightConfig(Base):
    __tablename__ = "light_config"
    intersection_id = Column(String, primary_key=True)
    green_time = Column(Integer, default=10)
    red_time = Column(Integer, default=10)
    updated_by = Column(String, nullable=True)
    updated_at = Column(String, nullable=True)
```

**Notas:**
- Importar `Base` desde database.py
- Usar `from sqlalchemy import Column, Integer, String, Text`
- Los modelos deben usar `from db.database import Base` para heredar

---

## Tarea 11: `backend/core/fault_handler.py` — Manejador de Fallos

**Archivo a crear:** `backend/core/fault_handler.py`

**Descripción:**
Simula fallos aleatorios en semáforos (interrupciones del sistema) con auto-recuperación.

**Clase `FaultHandler`:**
```python
import threading
import random
import time
from typing import Callable

class FaultHandler:
    def __init__(self, network, on_fault: Callable, on_restore: Callable):
        """
        network: instancia de TrafficNetwork
        on_fault: callback(intersection_id) cuando ocurre fallo
        on_restore: callback(intersection_id) cuando se recupera
        """
        self.network = network
        self.on_fault = on_fault
        self.on_restore = on_restore
        self._running = False
        self._thread = None

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._fault_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)

    def _fault_loop(self):
        while self._running:
            # Esperar intervalo aleatorio 15-30 segundos
            time.sleep(random.uniform(15, 30))
            if not self._running:
                break

            # Elegir intersección aleatoria
            nodes = list(self.network.nodes.values())
            if not nodes:
                continue

            intersection = random.choice(nodes)
            intersection.light.trigger_fault()

            # Notificar (el callback hace broadcast via WS)
            self.on_fault(intersection.id)

            # Auto-recuperación después de 5 segundos
            time.sleep(5)
            intersection.light.restore()
            self.on_restore(intersection.id)
```

**Notas:**
- `trigger_fault()` y `restore()` ya existen en `TrafficLight`
- Los callbacks `on_fault` y `on_restore` deben ser métodos del engine que hagan broadcast
- Importar de `config.py` los valores de intervalos

---

## Tarea 12: `backend/core/deadlock_detector.py` — Detección de Interbloqueos

**Archivo a crear:** `backend/core/deadlock_detector.py`

**Descripción:**
Detecta y resuelve interbloqueos usando timeout y rollback.

**Clase `DeadlockDetector`:**
```python
import threading
import time
from typing import Callable

class DeadlockDetector:
    """
    Implementa detección de deadlock con timeout por vehículo.
    Si un vehículo espera más de MAX_WAIT_TIME, se considera deadlock
    y se hace rollback (remover el vehículo de la cola).
    """
    MAX_WAIT_TIME = 10  # segundos antes de declarar deadlock

    def __init__(self, scheduler, on_deadlock: Callable):
        """
        scheduler: instancia de TrafficScheduler
        on_deadlock: callback(vehicle_id, intersection_id) cuando se detecta
        """
        self.scheduler = scheduler
        self.on_deadlock = on_deadlock
        self._running = False
        self._thread = None
        self._vehicle_timestamps = {}  # vehicle_id -> timestamp de cuando entró en cola

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._check_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)

    def register_vehicle(self, vehicle_id: str):
        """Registrar cuando un vehículo entra a esperar."""
        self._vehicle_timestamps[vehicle_id] = time.time()

    def unregister_vehicle(self, vehicle_id: str):
        """Remover vehículo cuando sale de la cola."""
        self._vehicle_timestamps.pop(vehicle_id, None)

    def _check_loop(self):
        while self._running:
            time.sleep(1)  # verificar cada segundo
            current_time = time.time()
            to_remove = []

            for vehicle_id, timestamp in self._vehicle_timestamps.items():
                if current_time - timestamp > self.MAX_WAIT_TIME:
                    to_remove.append(vehicle_id)

            for vehicle_id in to_remove:
                del self._vehicle_timestamps[vehicle_id]
                # TODO: Notificar al scheduler para remover el vehículo
                self.on_deadlock(vehicle_id, "timeout")
```

**Notas:**
- Este módulo es conceptualmente importante para el mapeo de SO (detección de deadlock)
- La implementación completa requiere integración con el scheduler para remover vehículos de las PriorityQueues
- El callback `on_deadlock` debe loguear en `event_log` con tipo `DEADLOCK`

---

## Tarea 13: `frontend/src/hooks/useWebSocket.js` — Hook de WebSocket

**Archivo a crear:** `frontend/src/hooks/useWebSocket.js`

**Descripción:**
Hook personalizado para conectarse al WebSocket del backend y mantener estado sincronizado.

**Implementación:**
```javascript
import { useEffect, useState, useRef, useCallback } from "react";

const WS_URL = import.meta.env.VITE_WS_URL || "ws://localhost:8000/ws";

export function useWebSocket() {
  const [state, setState] = useState({
    intersections: [],
    vehicles: [],
    alerts: [],
    connected: false,
    error: null
  });

  const wsRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);

  const connect = useCallback(() => {
    try {
      const ws = new WebSocket(WS_URL);

      ws.onopen = () => {
        setState(prev => ({ ...prev, connected: true, error: null }));
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.type === "STATE_UPDATE") {
            setState(prev => ({
              ...prev,
              intersections: data.intersections || [],
              vehicles: data.vehicles || [],
              alerts: data.alerts || []
            }));
          } else if (data.type === "FAULT") {
            setState(prev => ({
              ...prev,
              alerts: [...prev.alerts, { type: "FAULT", intersection: data.intersection_id, timestamp: data.timestamp }]
            }));
          } else if (data.type === "EMERGENCY") {
            setState(prev => ({
              ...prev,
              alerts: [...prev.alerts, { type: "EMERGENCY", vehicle: data.vehicle_id, timestamp: data.timestamp }]
            }));
          }
        } catch (e) {
          console.error("Error parsing WS message:", e);
        }
      };

      ws.onclose = () => {
        setState(prev => ({ ...prev, connected: false }));
        // Auto-reconnect after 2 seconds
        reconnectTimeoutRef.current = setTimeout(connect, 2000);
      };

      ws.onerror = (error) => {
        setState(prev => ({ ...prev, error: "WebSocket error" }));
      };

      wsRef.current = ws;
    } catch (e) {
      setState(prev => ({ ...prev, error: e.message }));
    }
  }, []);

  useEffect(() => {
    connect();
    return () => {
      if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current);
      if (wsRef.current) wsRef.current.close();
    };
  }, [connect]);

  return state;
}
```

**Notas:**
- Usar `useState` para mantener el último estado recibido
- Auto-reconectar si la conexión se pierde
- `VITE_WS_URL` variable de entorno para desarrollo
- El hook retorna: `{ intersections, vehicles, alerts, connected, error }`

---

## Tarea 14: `frontend/src/services/api.js` — Servicio API REST

**Archivo a crear:** `frontend/src/services/api.js`

**Descripción:**
Servicio para hacer llamadas REST al backend con manejo de autenticación.

**Implementación:**
```javascript
const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

class ApiService {
  constructor() {
    this.token = localStorage.getItem("token");
  }

  setToken(token) {
    this.token = token;
    if (token) {
      localStorage.setItem("token", token);
    } else {
      localStorage.removeItem("token");
    }
  }

  async request(method, path, body = null, requiresAuth = true) {
    const headers = { "Content-Type": "application/json" };
    if (requiresAuth && this.token) {
      headers["Authorization"] = `Bearer ${this.token}`;
    }

    const options = { method, headers };
    if (body && method !== "GET") {
      options.body = JSON.stringify(body);
    }

    const response = await fetch(`${API_BASE}${path}`, options);

    if (response.status === 401) {
      this.setToken(null);
      throw new Error("Unauthorized");
    }

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Request failed" }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
  }

  // Auth
  async login(username, password) {
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);
    // Note: fetch with FormData, not JSON
  }

  async register(username, password, role) {
    return this.request("POST", "/auth/register", { username, password, role }, false);
  }

  // Simulation
  async startSimulation() {
    return this.request("POST", "/simulation/start");
  }

  async stopSimulation() {
    return this.request("POST", "/simulation/stop");
  }

  async getStatus() {
    return this.request("GET", "/simulation/status");
  }

  async addVehicle(id, route, priority) {
    return this.request("POST", "/simulation/vehicle", { id, route, priority });
  }

  // Control
  async updateLightTiming(intersectionId, greenTime, redTime) {
    return this.request("PUT", `/control/lights/${intersectionId}/timing`, { green_time: greenTime, red_time: redTime });
  }

  async triggerFault(intersectionId) {
    return this.request("POST", `/control/lights/${intersectionId}/fault`);
  }

  async getLogs(eventType, limit) {
    const params = new URLSearchParams();
    if (eventType) params.append("event_type", eventType);
    if (limit) params.append("limit", limit);
    return this.request("GET", `/logs?${params.toString()}`);
  }
}

export const api = new ApiService();
```

**Notas:**
- Guardar token en localStorage para persistencia entre recargas
- `login()` debe usar FormData para compatibilidad con OAuth2PasswordRequestForm
- Lanzar `Error` en 401 para que el componente pueda redirigir a login

---

## Tarea 15: `frontend/src/components/LoginForm.jsx` — Formulario de Login

**Archivo a crear:** `frontend/src/components/LoginForm.jsx`

**Descripción:**
Formulario de login con validación JWT y persistencia del token.

**Requisitos UI:**
- Campos: username, password
- Botón "Iniciar Sesión"
- Mensajes de error
- Guardar token en localStorage al exitos
- Redirigir al grid principal tras login exitoso

**Implementación básica:**
```jsx
import { useState } from "react";
import { api } from "../services/api";

export function LoginForm({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const data = await api.login(username, password);
      api.setToken(data.access_token);
      localStorage.setItem("user_role", data.role);
      onLogin(data.role);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900">
      <form onSubmit={handleSubmit} className="bg-gray-800 p-8 rounded-lg shadow-xl w-96">
        <h1 className="text-2xl font-bold text-white mb-6">Traffic Control</h1>

        {error && (
          <div className="bg-red-500/20 border border-red-500 text-red-400 p-3 rounded mb-4">
            {error}
          </div>
        )}

        <div className="mb-4">
          <label className="block text-gray-300 mb-2">Usuario</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full bg-gray-700 text-white px-4 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        <div className="mb-6">
          <label className="block text-gray-300 mb-2">Contraseña</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full bg-gray-700 text-white px-4 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded font-medium transition disabled:opacity-50"
        >
          {loading ? "Iniciando..." : "Iniciar Sesión"}
        </button>
      </form>
    </div>
  );
}
```

**Notas:**
- Props: `onLogin(role)` callback que notifica al padre el rol del usuario
- Guardar rol en localStorage para verificar en componentes que requieren `control`
- Usar Tailwind para estilos (ya configurado en el proyecto)

---

## Tarea 16: `frontend/src/components/AlertBanner.jsx` — Banner de Alertas

**Archivo a crear:** `frontend/src/components/AlertBanner.jsx`

**Descripción:**
Componente para mostrar alertas de fallos de semáforo y emergencias en tiempo real.

**Requisitos UI:**
- Posición fija en la parte superior
- Colores según tipo: rojo para FAULT, amarillo/naranja para EMERGENCY
- Lista de alertas activas con timestamp
- Botón para dismiss individual o limpiar todas
- Animación de entrada (slide down)

**Estructura del dato:**
```javascript
{
  type: "FAULT" | "EMERGENCY",
  intersection?: string,
  vehicle?: string,
  timestamp: "ISO8601"
}
```

**Implementación sugerida:**
```jsx
import { useState } from "react";

export function AlertBanner({ alerts }) {
  const [dismissed, setDismissed] = useState([]);

  const visibleAlerts = alerts.filter(a => !dismissed.includes(a.timestamp));

  if (visibleAlerts.length === 0) return null;

  return (
    <div className="fixed top-0 left-0 right-0 z-50 p-4 space-y-2">
      {visibleAlerts.map((alert) => (
        <div
          key={alert.timestamp}
          className={`p-4 rounded-lg shadow-lg flex items-center justify-between ${
            alert.type === "FAULT"
              ? "bg-red-600 text-white"
              : "bg-yellow-500 text-black"
          }`}
        >
          <div className="flex items-center gap-3">
            <span className="text-2xl">{alert.type === "FAULT" ? "⚠️" : "🚨"}</span>
            <div>
              <p className="font-bold">
                {alert.type === "FAULT"
                  ? `Fallo en intersección ${alert.intersection}`
                  : `Vehículo de emergencia: ${alert.vehicle}`}
              </p>
              <p className="text-sm opacity-80">
                {new Date(alert.timestamp).toLocaleTimeString()}
              </p>
            </div>
          </div>
          <button
            onClick={() => setDismissed([...dismissed, alert.timestamp])}
            className="p-2 hover:bg-black/20 rounded"
          >
            ✕
          </button>
        </div>
      ))}
    </div>
  );
}
```

**Notas:**
- El componente es "dummy" - recibe `alerts` como prop desde el padre
- No maneja WebSocket directamente (el padre lo hace via `useWebSocket`)
- Usar transiciones CSS para animación de entrada/salida

---

## Resumen de Entrega 1

### Archivos a crear:

**Backend (8 archivos):**
1. `backend/config.py`
2. `backend/main.py`
3. `backend/auth/__init__.py`
4. `backend/auth/jwt_handler.py`
5. `backend/auth/roles.py`
6. `backend/api/__init__.py`
7. `backend/api/routes_auth.py`
8. `backend/api/routes_simulation.py`
9. `backend/api/routes_control.py`
10. `backend/api/websocket.py`
11. `backend/db/__init__.py`
12. `backend/db/database.py`
13. `backend/db/models.py`
14. `backend/core/fault_handler.py`
15. `backend/core/deadlock_detector.py`

**Frontend (4 archivos):**
16. `frontend/src/hooks/__init__.py`
17. `frontend/src/hooks/useWebSocket.js`
18. `frontend/src/services/__init__.py`
19. `frontend/src/services/api.js`
20. `frontend/src/components/__init__.py`
21. `frontend/src/components/LoginForm.jsx`
22. `frontend/src/components/AlertBanner.jsx`

**Modificar (2 archivos):**
23. `frontend/src/App.jsx` - Actualizar para usar LoginForm y AlertBanner

### Criterios de Aceptación:
- [ ] Backend inicia sin errores con `uvicorn main:app --reload`
- [ ] `POST /auth/register` crea usuarios
- [ ] `POST /auth/login` retorna JWT válido
- [ ] Rutas protegidas requieren token JWT correcto
- [ ] Rutas `control` rechaza usuarios con rol `viewer`
- [ ] WebSocket `/ws` acepta conexiones y recibe broadcasts
- [ ] `POST /simulation/start` inicia el motor
- [ ] Frontend conecta a WebSocket y recibe estado
- [ ] LoginForm guarda token y llama onLogin
- [ ] AlertBanner muestra alertas recibidas
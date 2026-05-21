# Sistemas-de-Gestion-Trafico-Urbano-OS

# 🚦 Sistema de Gestión de Tráfico Urbano

### Arquitectura del Proyecto — Sistemas Operativos

**Estado actual:** [x] Backend completo [x] Frontend completo [x] Integración end-to-end

**Stack tecnológico:**
- **Backend:** Python 3.12 — FastAPI + threading + asyncio
- **Frontend:** React 19 + Vite 8 + Tailwind v4
- **Persistencia:** SQLite con SQLAlchemy
- **Comunicación:** WebSockets nativos + API REST con JWT

---

## 1. Visión General

Sistema que modela una red de intersecciones urbanas con vehículos concurrentes, semáforos sincronizados, prioridad para emergencias, detección de fallos y control de acceso por roles.

**Stack tecnológico:**

- **Backend:** Python 3.11 (FastAPI + threading + asyncio)
- **Frontend:** React + Vite (WebSockets para tiempo real)
- **Persistencia:** SQLite (simple, sin servidor, suficiente para el scope académico)
- **Comunicación en tiempo real:** WebSockets nativos de FastAPI

---

## 2. Conceptos de SO y su Mapeo en Código

| Concepto SO                 | Implementación Python                                           |
| --------------------------- | --------------------------------------------------------------- |
| **Semáforos**               | `threading.Semaphore` — controla acceso a intersecciones        |
| **Procesos concurrentes**   | `threading.Thread` — un thread por vehículo activo              |
| **Priority Scheduling**     | `queue.PriorityQueue` — vehículos de emergencia con prioridad 0 |
| **Interbloqueo (deadlock)** | Algoritmo de detección con timeout + rollback                   |
| **Interrupciones**          | `threading.Event` — simula fallo de semáforo                    |
| **Dominios de seguridad**   | JWT tokens con roles: `control` / `viewer`                      |

---

## 3. Estructura de Carpetas

```
traffic-system/
├── backend/
│   ├── main.py                  # Entry point FastAPI
│   ├── config.py                # Configuración global
│   ├── auth/
│   │   ├── jwt_handler.py       # Generación y validación de tokens JWT
│   │   └── roles.py             # Decoradores de autorización por rol
│   ├── core/
│   │   ├── intersection.py      # Clase Intersection (recurso compartido)
│   │   ├── vehicle.py           # Clase Vehicle (proceso concurrente)
│   │   ├── traffic_light.py     # Clase TrafficLight (semáforo SO)
│   │   ├── scheduler.py         # Priority scheduler para vehículos
│   │   ├── deadlock_detector.py # Detección y resolución de interbloqueos
│   │   └── fault_handler.py     # Módulo de interrupciones / fallos
│   ├── simulation/
│   │   ├── engine.py            # Motor principal de simulación
│   │   └── network.py           # Grafo de intersecciones conectadas
│   ├── api/
│   │   ├── routes_auth.py       # POST /login, POST /register
│   │   ├── routes_control.py    # PUT /lights/{id} (solo rol "control")
│   │   ├── routes_simulation.py # POST /start, POST /stop, GET /status
│   │   └── websocket.py         # WS /ws — stream de estado en tiempo real
│   └── db/
│       ├── database.py          # Conexión SQLite con SQLAlchemy
│       └── models.py            # Modelos: User, EventLog, LightConfig
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── IntersectionGrid.jsx  # Visualización de la red
│   │   │   ├── TrafficLight.jsx      # Semáforo visual
│   │   │   ├── VehicleMarker.jsx     # Vehículo en movimiento
│   │   │   ├── ControlPanel.jsx      # Panel admin (solo rol "control")
│   │   │   ├── AlertBanner.jsx       # Alertas de fallos / emergencias
│   │   │   └── LoginForm.jsx
│   │   ├── hooks/
│   │   │   └── useWebSocket.js       # Hook para conexión WS
│   │   └── services/
│   │       └── api.js                # Llamadas REST al backend
│   └── vite.config.js
├── requirements.txt
├── package.json
└── README.md
```

---

## 4. Módulos del Backend — Detalle

### 4.1 `core/traffic_light.py` — Semáforo (concepto SO)

```python
import threading
import time

class TrafficLight:
    """
    Representa un semáforo como recurso compartido del SO.
    Usa threading.Semaphore para controlar acceso a la intersección.
    """
    def __init__(self, intersection_id: str, green_time: int = 10):
        self.id = intersection_id
        self.state = "RED"           # RED | GREEN | YELLOW | FAULT
        self.green_time = green_time # Modificable solo por rol "control"
        self.semaphore = threading.Semaphore(1)  # 1 vehículo a la vez
        self.fault_event = threading.Event()     # Simula interrupción de fallo
        self._lock = threading.Lock()

    def acquire(self, vehicle_id: str, timeout: float = 5.0) -> bool:
        """Vehículo intenta cruzar la intersección."""
        acquired = self.semaphore.acquire(timeout=timeout)
        if not acquired:
            # Posible deadlock: reportar al detector
            return False
        return True

    def release(self):
        self.semaphore.release()

    def trigger_fault(self):
        """Simula interrupción de sensor: fallo del semáforo."""
        with self._lock:
            self.state = "FAULT"
        self.fault_event.set()

    def restore(self):
        with self._lock:
            self.state = "RED"
        self.fault_event.clear()
```

---

### 4.2 `core/vehicle.py` — Vehículo (proceso concurrente)

```python
import threading
from enum import IntEnum

class Priority(IntEnum):
    EMERGENCY = 0   # Ambulancia, bomberos, policía
    HIGH      = 1   # Transporte público
    NORMAL    = 2   # Vehículo regular

class Vehicle(threading.Thread):
    """
    Cada vehículo es un Thread independiente (proceso concurrente).
    Navega la red de intersecciones usando el scheduler de prioridad.
    """
    def __init__(self, vehicle_id: str, route: list, priority: Priority, scheduler):
        super().__init__(daemon=True)
        self.vehicle_id = vehicle_id
        self.route = route           # Lista de intersection_ids a cruzar
        self.priority = priority
        self.scheduler = scheduler
        self.current_position = 0
        self.status = "WAITING"      # WAITING | MOVING | DONE | BLOCKED

    def run(self):
        """Lógica principal del thread: navegar la ruta."""
        for intersection_id in self.route:
            self.status = "WAITING"
            # Encolar en el priority scheduler
            self.scheduler.enqueue(self, intersection_id)
            # Esperar turno (bloqueante hasta ser despachado)
            self.scheduler.wait_for_dispatch(self.vehicle_id)
            self.status = "MOVING"
            self.current_position += 1
        self.status = "DONE"
```

---

### 4.3 `core/scheduler.py` — Priority Scheduling

```python
import queue
import threading

class TrafficScheduler:
    """
    Implementa Priority Scheduling para intersecciones.
    Vehículos de emergencia (prioridad 0) siempre van primero.
    """
    def __init__(self):
        # PriorityQueue: (prioridad, timestamp, vehicle)
        self._queues: dict[str, queue.PriorityQueue] = {}
        self._dispatch_events: dict[str, threading.Event] = {}
        self._lock = threading.Lock()

    def enqueue(self, vehicle, intersection_id: str):
        import time
        with self._lock:
            if intersection_id not in self._queues:
                self._queues[intersection_id] = queue.PriorityQueue()
            if vehicle.vehicle_id not in self._dispatch_events:
                self._dispatch_events[vehicle.vehicle_id] = threading.Event()

        entry = (vehicle.priority, time.time(), vehicle)
        self._queues[intersection_id].put(entry)

    def dispatch_next(self, intersection_id: str):
        """El motor llama esto cuando el semáforo abre."""
        if intersection_id in self._queues:
            try:
                _, _, vehicle = self._queues[intersection_id].get_nowait()
                self._dispatch_events[vehicle.vehicle_id].set()
            except queue.Empty:
                pass

    def wait_for_dispatch(self, vehicle_id: str):
        event = self._dispatch_events.get(vehicle_id)
        if event:
            event.wait()
            event.clear()
```

---

### 4.4 `core/fault_handler.py` — Módulo de Interrupciones

```python
import threading
import random
import time
from typing import Callable

class FaultHandler:
    """
    Simula fallos aleatorios en semáforos (interrupciones del sistema).
    Al detectar un fallo, propaga alerta a intersecciones vecinas.
    """
    def __init__(self, network, on_fault: Callable, on_restore: Callable):
        self.network = network       # Grafo de intersecciones
        self.on_fault = on_fault     # Callback → notificar al frontend via WS
        self.on_restore = on_restore
        self._running = False

    def start(self):
        self._running = True
        t = threading.Thread(target=self._fault_loop, daemon=True)
        t.start()

    def stop(self):
        self._running = False

    def _fault_loop(self):
        while self._running:
            time.sleep(random.uniform(15, 30))  # Fallo cada 15-30 segundos
            if not self._running:
                break
            # Elegir intersección aleatoria para fallar
            intersection = random.choice(list(self.network.nodes.values()))
            intersection.light.trigger_fault()
            self.on_fault(intersection.id)

            # Auto-recuperación después de 5 segundos
            time.sleep(5)
            intersection.light.restore()
            self.on_restore(intersection.id)
```

---

### 4.5 `auth/jwt_handler.py` — Dominios de Seguridad

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "traffic-system-secret"
ALGORITHM = "HS256"
ROLES = ["viewer", "control"]  # "control" puede modificar semáforos

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_token(user_id: str, role: str) -> str:
    payload = {
        "sub": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=8)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def require_role(required_role: str):
    """Decorador de dependencia FastAPI para proteger rutas por rol."""
    def dependency(token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("role") != required_role:
                raise HTTPException(status_code=403, detail="Rol insuficiente")
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Token inválido")
    return dependency
```

---

### 4.6 `api/routes_control.py` — Ruta Protegida por Rol

```python
from fastapi import APIRouter, Depends
from auth.jwt_handler import require_role

router = APIRouter(prefix="/control", tags=["Control"])

@router.put("/lights/{intersection_id}/timing")
def update_timing(
    intersection_id: str,
    green_time: int,
    red_time: int,
    user=Depends(require_role("control"))  # Solo rol "control" puede acceder
):
    """Modificar tiempos de espera del semáforo en una intersección."""
    # ...actualizar en la simulación en tiempo real
    return {"status": "updated", "intersection": intersection_id}
```

---

### 4.7 `api/websocket.py` — Stream en Tiempo Real

```python
from fastapi import WebSocket, WebSocketDisconnect
import json

class ConnectionManager:
    def __init__(self):
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    async def broadcast(self, data: dict):
        msg = json.dumps(data)
        for ws in self.active:
            try:
                await ws.send_text(msg)
            except:
                self.active.remove(ws)

manager = ConnectionManager()

# El motor de simulación llama a manager.broadcast() en cada tick
# Formato del mensaje:
# {
#   "type": "STATE_UPDATE" | "FAULT" | "EMERGENCY" | "VEHICLE_DONE",
#   "intersections": [...],
#   "vehicles": [...],
#   "timestamp": "..."
# }
```

---

## 5. Modelo de Datos (SQLite)

```sql
-- Usuarios del sistema
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('viewer', 'control'))
);

-- Log de eventos (auditoría)
CREATE TABLE event_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    event_type TEXT NOT NULL,  -- FAULT | EMERGENCY | CONFIG_CHANGE | DEADLOCK
    intersection_id TEXT,
    vehicle_id TEXT,
    details TEXT,              -- JSON con contexto adicional
    user_id TEXT               -- Quién realizó cambios de configuración
);

-- Configuración de semáforos (persistente)
CREATE TABLE light_config (
    intersection_id TEXT PRIMARY KEY,
    green_time INTEGER DEFAULT 10,
    red_time INTEGER DEFAULT 10,
    updated_by TEXT,
    updated_at TEXT
);
```

---

## 6. API REST — Endpoints

| Método | Ruta                           | Rol requerido | Descripción                                     |
| ------ | ------------------------------ | ------------- | ----------------------------------------------- |
| `POST` | `/auth/login`                  | —             | Login, retorna JWT                              |
| `POST` | `/auth/register`               | —             | Registro de usuario                             |
| `POST` | `/simulation/start`            | `control`     | Inicia la simulación (grid 3×3 + FaultHandler + DeadlockDetector) |
| `POST` | `/simulation/stop`             | `control`     | Detiene la simulación                           |
| `GET`  | `/simulation/status`           | `viewer`      | Estado actual: intersecciones, vehículos, posiciones |
| `GET`  | `/simulation/metrics`          | `viewer`      | Métricas SO: mutex, colas, tiempos de espera    |
| `POST` | `/simulation/vehicle`          | `control`     | Agregar vehículo manualmente                    |
| `POST` | `/simulation/scenario`         | `control`     | Ejecutar demo: mutex_demo, priority_demo, deadlock_demo |
| `PUT`  | `/control/lights/{id}/timing`  | `control`     | Modificar green_time y red_time del semáforo    |
| `POST` | `/control/lights/{id}/fault`   | `control`     | Simular fallo manual en semáforo                |
| `GET`  | `/control/logs`                | `control`     | Historial de eventos (FAULT, DEADLOCK, CONFIG_CHANGE) |
| `WS`   | `/ws`                          | —             | Stream en tiempo real: STATE_UPDATE, FAULT, RESTORE, DEADLOCK |

---

## 7. Flujo de Demo para Sustentación

```
1. Login → "Sistema con control de acceso basado en roles (viewer/control)"
2. Iniciar simulación → grid 3×3 con semáforos de 3 luces, calles y marcas viales
3. Panel de Métricas SO muestra: 🔒 mutex (libre/ocupado), colas, tiempos de espera

4. [Botón "Demo: Exclusión Mutua"] → 3 autos compiten por misma intersección
   → Solo 1 cruza, los otros esperan → 🔒 en el grid + métricas: mutex TOMADO

5. [Botón "Demo: Prioridad"] → 1 🚑 ambulancia + 2 autos normales
   → Ambulancia (P0) despachada primero pese a llegar después → Priority Scheduling

6. [Botón "Demo: Deadlock"] → 2 vehículos con rutas que se cruzan
   → A los 10s el DeadlockDetector detecta → rollback → broadcast DEADLOCK

7. Fallos automáticos → cada 15-30s un semáforo falla (FAULT)
   → Overlay rojo pulsante + AlertBanner → auto-recuperación a los 5s

8. Panel de control → modificar green_time/red_time en tiempo real
```

---

## 8. Frontend — Componentes Clave

### `useWebSocket.js`

```javascript
import { useEffect, useState } from "react";

export function useWebSocket(url) {
  const [state, setState] = useState({
    intersections: [],
    vehicles: [],
    alerts: [],
  });

  useEffect(() => {
    const ws = new WebSocket(url);
    ws.onmessage = (e) => {
      const data = JSON.parse(e.data);
      setState((prev) => ({ ...prev, ...data }));
    };
    return () => ws.close();
  }, [url]);

  return state;
}
```

### `IntersectionGrid.jsx`

- Grilla CSS de N×M intersecciones
- Cada celda tiene un `<TrafficLight />` con color según estado (`GREEN` / `RED` / `YELLOW` / `FAULT`)
- `<VehicleMarker />` se anima sobre la grilla usando `position: absolute` + CSS transitions

### `ControlPanel.jsx`

- Solo visible si `jwt.role === "control"`
- Sliders para `green_time` / `red_time` por intersección
- Botón "Simular Fallo" y "Agregar Emergencia"

---

## 9. Plan de Implementación (Orden sugerido)

| Fase  | Qué construir                                               | Estimado |
| ----- | ----------------------------------------------------------- | -------- |
| **1** | Modelos core: `TrafficLight`, `Vehicle`, `TrafficScheduler` | 2–3h     |
| **2** | Motor de simulación + lógica de concurrencia básica         | 2–3h     |
| **3** | FastAPI: rutas REST + WebSocket broadcast                   | 2h       |
| **4** | Auth JWT + protección de rutas por rol                      | 1–2h     |
| **5** | `FaultHandler` + `DeadlockDetector`                         | 1–2h     |
| **6** | Frontend: grid + websocket hook + semáforos visuales        | 3–4h     |
| **7** | Panel de control + login + protección por rol               | 2h       |
| **8** | SQLite: event log + persistencia de configs                 | 1h       |
| **9** | Pruebas integradas + ajustes visuales                       | 2h       |

**Total estimado: ~16–19 horas de trabajo en equipo**

---

## 10. Dependencias

### `requirements.txt`

```
fastapi==0.111.0
uvicorn==0.30.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
sqlalchemy==2.0.30
websockets==12.0
python-multipart==0.0.9
```

### `package.json` (frontend)

```json
{
  "dependencies": {
    "react": "^18.3.0",
    "react-dom": "^18.3.0"
  },
  "devDependencies": {
    "vite": "^5.0.0",
    "@vitejs/plugin-react": "^4.0.0"
  }
}
```

---

## 11. Comandos para Iniciar

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

---

_Documento generado como guía de implementación para el agente de código._

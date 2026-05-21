# Arquitectura del Sistema - ENTREGA 1
## Sistema de Gestión de Tráfico Urbano

---

## 1. VISIÓN GENERAL DEL SISTEMA

El Sistema de Gestión de Tráfico Urbano es una aplicación académico que modela 
el control de tráfico de una ciudad usando conceptos de Sistemas Operativos:

- **Vehículos** = Hilos/Procesos independientes (daemon threads)
- **Semáforos** = Recursos con mutex (threading.Semaphore)
- **Scheduler** = Planificador por prioridad (queue.PriorityQueue)
- **FaultHandler** = Interrupciones simuladas (threading.Event)
- **DeadlockDetector** = Detección de interbloqueos con timeout

### Stack Tecnológico

| Capa | Tecnología |
|------|------------|
| Backend API | FastAPI + Uvicorn |
| Auth | JWT (python-jose) + bcrypt (passlib) |
| Database | SQLite + SQLAlchemy |
| Real-time | WebSocket (broadcast) |
| Frontend | React 19 + Vite + TailwindCSS v4 |

---

## 2. DIAGRAMA DE ARQUITECTURA

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           FRONTEND (React)                               │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                         App.jsx                                 │    │
│  │  ┌──────────────┐  ┌────────────────┐  ┌──────────────────┐   │    │
│  │  │  LoginForm   │  │ useWebSocket() │  │  AlertBanner     │   │    │
│  │  └──────┬───────┘  └───────┬────────┘  └────────┬─────────┘   │    │
│  │         │                  │                   │              │    │
│  │         │    ┌────────────┴────────────┐       │              │    │
│  │         │    │                         │       │              │    │
│  │         v    v                         v       v              │    │
│  │  ┌─────────────────────────────────────────────────────┐     │    │
│  │  │              api.js (ApiService)                     │     │    │
│  │  │   - REST calls (fetch)                              │     │    │
│  │  │   - JWT token management                            │     │    │
│  │  │   - FormData for OAuth2 login                       │     │    │
│  │  └─────────────────────────────────────────────────────┘     │    │
│  └──────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────┬────┘
                                                                        │
                                                        HTTP / WebSocket
                                                                        │
┌───────────────────────────────────────────────────────────────────────┴──┐
│                              BACKEND (FastAPI)                            │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                         main.py (Entry Point)                         │  │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │  │
│  │  │  lifespan(): Base.metadata.create_all() - crea tablas SQLite     │ │  │
│  │  └──────────────────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                    │                                        │
│         ┌──────────────────────────┼──────────────────────────┐         │
│         │                          │                          │              │
│         v                          v                          v              │
│  ┌─────────────┐          ┌─────────────┐          ┌─────────────┐     │
│  │ routes_auth │          │routes_simul  │          │routes_ctrl  │     │
│  │   (JWT)    │          │(Simulation) │          │ (Control)   │     │
│  └──────┬──────┘          └──────┬──────┘          └──────┬──────┘     │
│         │                         │                         │              │
│         │    ┌───────────────────┴───────────────────┐    │              │
│         │    │                                       │    │              │
│         v    v                                       v    v              │
│  ┌─────────────────────────────────────────────────────────────┐        │
│  │                    api/websocket.py                         │        │
│  │              ConnectionManager (broadcast)                  │        │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐              │        │
│  │  │ connect() │  │broadcast()│  │disconnect()│              │        │
│  │  └───────────┘  └───────────┘  └───────────┘              │        │
│  └─────────────────────────────────────────────────────────────┘        │
│                         │                                                │
│  ═══════════════════════╪══════════════════════════════════════════════  │
│                         │                                                │
│  ┌──────────────────────┴──────────────────────────────────────────┐  │
│  │                    SIMULATION LAYER (Kernel)                       │  │
│  │  ┌─────────────────┐              ┌─────────────────┐            │  │
│  │  │SimulationEngine │              │  FaultHandler   │            │  │
│  │  │   (_loop)       │              │ (thread demon)  │            │  │
│  │  │   tick=1s       │              │ cada 15-30s      │            │  │
│  │  └────────┬────────┘              └────────┬────────┘            │  │
│  │           │                                │                      │  │
│  │           └────────────┬───────────────────┘                      │  │
│  │                        v                                          │  │
│  │  ┌─────────────────────────────────────────────────────────┐      │  │
│  │  │              TrafficNetwork (RAG)                       │      │  │
│  │  │  nodes: {intersection_id: Intersection}                  │      │  │
│  │  │  adjacency_list: {id: [neighbor_ids]}                    │      │  │
│  │  └─────────────────────────────────────────────────────────┘      │  │
│  └────────────────────────────────────────────────────────────────┘      │
│                         │                                                │
│  ═══════════════════════╪══════════════════════════════════════════════  │
│                         │                                                │
│  ┌──────────────────────┴──────────────────────────────────────────┐  │
│  │                    CORE LAYER (SO Abstractions)                  │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌──────────┐  │  │
│  │  │  Vehicle   │  │ TrafficLight│  │ Scheduler  │  │Intersection│  │  │
│  │  │ (Thread)   │  │ (Semaphore) │  │(PQueue)    │  │  (Node)   │  │  │
│  │  └────────────┘  └────────────┘  └────────────┘  └──────────┘  │  │
│  │                                                                  │  │
│  │  ┌──────────────────────────────────────────────────────────┐   │  │
│  │  │              DeadlockDetector (timeout 10s)               │   │  │
│  │  └──────────────────────────────────────────────────────────┘   │  │
│  └────────────────────────────────────────────────────────────────┘      │
│                         │                                                │
│  ═══════════════════════╪══════════════════════════════════════════════  │
│                         │                                                │
│  ┌──────────────────────┴──────────────────────────────────────────┐  │
│  │                       DATA LAYER (SQLite)                         │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────────┐             │  │
│  │  │   Users    │  │ EventLog   │  │  LightConfig   │             │  │
│  │  │ (auth)    │  │ (audit)   │  │ (config)      │             │  │
│  │  └────────────┘  └────────────┘  └────────────────┘             │  │
│  └─────────────────────────────────────────────────────────────────┘      │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. FLUJOS PRINCIPALES

### 3.1 Flujo de Autenticación JWT

```
┌─────────┐         ┌─────────────┐        ┌────────────────┐
│Usuario  │         │ LoginForm   │        │   api.js       │
└────┬────┘         └──────┬──────┘        └───────┬────────┘
     │                     │                      │
     │ 1. username, password                     │
     │────────────────────>│                      │
     │                     │                      │
     │                     │ 2. api.login()      │
     │                     │────────────────────>│
     │                     │                      │
     │                     │        3. POST /auth/login
     │                     │        (FormData)   │
     │                     │<────────────────────│
     │                     │                      │
     │                     │ 4. {access_token, role}
     │                     │<────────────────────│
     │                     │                      │
     │ 5. {access_token}   │                      │
     │<────────────────────│                      │
     │                     │                      │
     │ 6. localStorage.setItem("token", token)    │
     │ 7. localStorage.setItem("user_role", role)  │
     │ 8. onLogin(role)   │                      │
     │────────────────────>│                      │
                          │                      │
                          ▼                      │
                   ┌─────────────┐              │
                   │   App.jsx   │              │
                   └──────┬─────┘              │
                          │                   │
                          │ 9. useWebSocket()  │
                          │    + API calls    │
                          │    with Bearer    │
                          └───────────────────┘
```

### 3.2 Flujo de Inicio de Simulación

```
┌─────────┐         ┌─────────────┐        ┌────────────────┐
│Usuario  │         │   App.jsx   │        │routes_simul    │
└────┬────┘         └──────┬──────┘        └───────┬────────┘
     │                     │                      │
     │ 1. click "Iniciar"  │                      │
     │────────────────────>│                      │
     │                     │                      │
     │                     │ 2. POST /simulation/start
     │                     │─────────────────────>│
     │                     │                      │
     │                     │        3. Crea TrafficNetwork (3x3)
     │                     │        4. Crea SimulationEngine
     │                     │        5. Crea TrafficScheduler
     │                     │        6. Inicia FaultHandler
     │                     │        7. engine.start() → _loop()
     │                     │                      │
     │                     │        8. {status: "started", intersections: 9}
     │                     │<────────────────────│
     │                     │                      │
     │ 9. simulationRunning = true                 │
     │<────────────────────│                      │
     │                     │                      │
     │                     │        10. _loop() cada 1s
     │                     │        11. engine.state_snapshot()
     │                     │        12. manager.broadcast(state)
     │                     │<────────────────────│
     │                     │                      │
     │ 13. WS: STATE_UPDATE │                      │
     │<────────────────────│                      │
                          │                      │
                          ▼                      │
                   ┌─────────────┐              │
                   │ useWebSocket│              │
                   └──────┬─────┘              │
                          │                   │
                          │ 14. setState()     │
                          │    intersections  │
                          │    vehicles       │
                          └───────────────────┘
```

### 3.3 Flujo de Fault (Interrupcción)

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  FaultHandler    │     │ TrafficLight     │     │ConnectionManager │
│  (_fault_loop)   │     │                 │     │                 │
└────────┬─────────┘     └────────┬─────────┘     └────────┬────────┘
         │                        │                        │
         │ 1. time.sleep(15-30s)  │                        │
         │    aleatorio           │                        │
         │                        │                        │
         │ 2. select intersection│                        │
         │ 3. light.trigger_fault()                        │
         │──────────────────────>│                        │
         │                        │                        │
         │ 4. on_fault(id)        │                        │
         │<═══════════════════════│                        │
         │                        │                        │
         │ 5. manager.broadcast() │                        │
         │═══════════════════════│══════════════════════>│
         │                        │                        │
         │                        │ 6. ws.send_text() a     │
         │                        │    todos los clientes  │
         │                        │                        │
         │ 7. time.sleep(5s)      │                        │
         │                        │                        │
         │ 8. light.restore()      │                        │
         │──────────────────────>│                        │
         │                        │                        │
         │ 9. on_restore(id)      │                        │
         │<═══════════════════════│                        │
         │                        │                        │
         │ 10. broadcast RESTORE   │                        │
         │═══════════════════════│══════════════════════>│
         │                        │                        │
```

### 3.4 Flujo de Deadlock Detection

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Vehicle         │     │DeadlockDetector  │     │ EventLog (DB)   │
│  (Thread)        │     │                 │     │                 │
└────────┬─────────┘     └────────┬─────────┘     └────────┬────────┘
         │                        │                        │
         │ 1. scheduler.enqueue() │                        │
         │<──────────────────────│                        │
         │                        │                        │
         │ 2. register_vehicle() │                        │
         │──────────────────────>│                        │
         │                        │                        │
         │ 3. wait_for_dispatch() │                        │
         │<──────────────────────│                        │
         │                        │                        │
         │ 4. _check_loop() cada 1s│                        │
         │<──────────────────────│                        │
         │                        │                        │
         │ 5. timeout? (10s)     │                        │
         │     NO → continúa     │                        │
         │                        │                        │
         │ 6. timeout? (10s)     │                        │
         │     SÍ →              │                        │
         │                        │                        │
         │ 7. on_deadlock(vehicle_id, "timeout")          │
         │──────────────────────>│───────────────────────>│
         │                        │                        │
         │                        │ 8. EventLog.create()  │
         │                        │    type: "DEADLOCK"    │
         │                        │<──────────────────────│
```

---

## 4. MAPEO DE CONCEPTOS DE SISTEMAS OPERATIVOS

| Concepto SO | Implementación en el Proyecto |
|-------------|-------------------------------|
| **Proceso/Hilo** | `Vehicle` = `threading.Thread` (daemon) |
| **PCB (Process Control Block)** | `Vehicle` attributes: vehicle_id, route, priority, status |
| **Recurso** | `TrafficLight` = `threading.Semaphore(1)` (mutex) |
| **Monitor** | `TrafficLight._lock` = `threading.Lock` protege estado |
| **ISR (Interrupt Service Routine)** | `TrafficLight.trigger_fault()`, `.restore()` |
| **Ready Queue** | `TrafficScheduler._queues[intersection_id]` = `PriorityQueue` |
| **Dispatcher** | `scheduler.dispatch_next()` otorga recurso al de mayor prioridad |
| **Planificador** | `TrafficScheduler` usa `(priority, timestamp, vehicle)` |
| **Deadlock Detection** | `DeadlockDetector` con timeout de 10s |
| **Kernel Tick** | `SimulationEngine._loop()` cada 1 segundo |
| **Context Switch** | Vehicle pasa de WAITING → MOVING cuando recibe dispatch |

---

## 5. COMUNICACIÓN ENTRE MÓDULOS

### 5.1 Tabla de Dependencias

| Módulo | Depende de | Tipo de Dependencia |
|--------|------------|---------------------|
| main.py | routes_auth, routes_simulation, routes_control, websocket, db.database | Imports |
| routes_auth | db.database, db.models, auth.jwt_handler | Imports |
| routes_simulation | auth.roles, core.vehicle, simulation.engine, simulation.network, core.scheduler, api.websocket | Imports |
| routes_control | auth.roles, db.database, db.models, api.routes_simulation (get_engine) | Imports |
| websocket | auth.jwt_handler | Import (decode_token) |
| fault_handler | config, simulation.network | Imports |
| deadlock_detector | simulation.network, core.scheduler | Imports |
| engine | simulation.network, core.scheduler, core.vehicle | Imports |
| network | core.intersection | Import |

### 5.2 Variables Globales Compartidas

| Variable | Módulo | Tipo | Usado por |
|----------|--------|------|-----------|
| _engine | routes_simulation | SimulationEngine | routes_control (vía get_engine) |
| _network | routes_simulation | IntersectionNetwork | routes_control |
| _scheduler | routes_simulation | TrafficScheduler | routes_control |
| manager | websocket | ConnectionManager | routes_simulation, routes_control |

### 5.3 Callbacks

| Módulo | Callback | Hacia | Propósito |
|--------|----------|-------|-----------|
| FaultHandler | on_fault(intersection_id) | SimulationEngine._broadcast_fault() | Notificar fault |
| FaultHandler | on_restore(intersection_id) | SimulationEngine._broadcast_restore() | Notificar recovery |
| DeadlockDetector | on_deadlock(vehicle_id, reason) | SimulationEngine._log_deadlock() | Registrar deadlock |

---

## 6. ENDPOINTS Y WEBSOCKET

### 6.1 REST API

| Método | Endpoint | Rol | Descripción |
|--------|----------|-----|-------------|
| POST | /auth/register | - | Registro de usuario |
| POST | /auth/login | - | Login (FormData OAuth2) |
| POST | /simulation/start | control | Iniciar simulación |
| POST | /simulation/stop | control | Detener simulación |
| GET | /simulation/status | viewer, control | Estado actual |
| POST | /simulation/vehicle | control | Agregar vehículo |
| PUT | /control/lights/:id/timing | control | Actualizar tiempos |
| POST | /control/lights/:id/fault | control | Trigger fault manual |
| GET | /control/lights | control | Lista configs |
| GET | /control/logs | control | Obtener logs |
| GET | / | - | Health check |
| GET | /health | - | Health check detallado |

### 6.2 WebSocket

| Endpoint | Dirección | Propósito |
|----------|-----------|-----------|
| /ws | Bidireccional | Broadcast de estado en tiempo real |

**Mensajes del servidor al cliente:**

```javascript
// STATE_UPDATE (cada tick)
{
  "type": "STATE_UPDATE",
  "intersections": [
    {
      "id": "N0",
      "state": "GREEN", // GREEN | YELLOW | RED | FAULT
      "position": {"x": 0, "y": 0},
      "vehicle_count": 2
    }
  ],
  "vehicles": [
    {
      "id": "V1",
      "status": "MOVING", // WAITING | MOVING | DONE | BLOCKED
      "position": 1,
      "route": ["N0", "N1", "N2"],
      "priority": "HIGH" // EMERGENCY | HIGH | NORMAL
    }
  ],
  "alerts": [],
  "timestamp": "2026-05-14T10:30:00Z"
}

// FAULT
{
  "type": "FAULT",
  "intersection_id": "N1",
  "timestamp": "2026-05-14T10:30:00Z"
}

// EMERGENCY
{
  "type": "EMERGENCY",
  "vehicle_id": "V1",
  "timestamp": "2026-05-14T10:30:00Z"
}
```

---

## 7. MODELOS DE BASE DE DATOS

### 7.1 User
```python
class User(Base):
    __tablename__ = "users"
    id: str (PK)
    username: str (unique)
    password_hash: str
    role: str  # "viewer" | "control"
```

### 7.2 EventLog
```python
class EventLog(Base):
    __tablename__ = "event_log"
    id: int (PK, autoincrement)
    timestamp: str  # ISO8601
    event_type: str  # FAULT | EMERGENCY | CONFIG_CHANGE | DEADLOCK
    intersection_id: str | None
    vehicle_id: str | None
    details: str | None  # JSON
    user_id: str | None
```

### 7.3 LightConfig
```python
class LightConfig(Base):
    __tablename__ = "light_config"
    intersection_id: str (PK)
    green_time: int (default: 10)
    red_time: int (default: 10)
    updated_by: str | None
    updated_at: str | None  # ISO8601
```

---

## 8. SEGURIDAD Y ROLES

### 8.1 Roles

| Rol | Permisos |
|-----|----------|
| viewer | GET /simulation/status, GET (solo lectura) |
| control | TODOS los endpoints incluyendo modificaciones |

### 8.2 Flujo de Autorización

```
Request con Bearer Token
          │
          v
   decode_token(token)
          │
          v
   get_current_user(token)
          │
          v
   require_role("control")
          │
    ┌─────┴─────┐
    │           │
  OK (200)   FAIL (403)
    │           │
    v           v
Continúa    Forbidden
```

---

## 9. VARIABLES DE ENTORNO

| Variable | Default | Backend/Frontend | Descripción |
|----------|---------|------------------|-------------|
| DB_PATH | traffic.db | Backend | Ruta SQLite |
| JWT_SECRET | traffic-system-secret | Backend | Clave JWT |
| API_HOST | 0.0.0.0 | Backend | Host API |
| API_PORT | 8000 | Backend | Puerto API |
| VITE_API_URL | http://localhost:8000 | Frontend | Base URL API |
| VITE_WS_URL | ws://localhost:8000/ws | Frontend | WebSocket URL |

---

## 10. ESTRUCTURA DE DIRECTORIOS

```
Sistemas-de-Gestion-Trafico-Urbano-OS/
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes_auth.py       # Endpoints de autenticación (register, login)
│   │   ├── routes_simulation.py # Endpoints de simulación (start, stop, status, vehicle)
│   │   ├── routes_control.py     # Control de semáforos y logs
│   │   └── websocket.py          # ConnectionManager y endpoint WebSocket /ws
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── jwt_handler.py        # create_token(), decode_token(), get_current_user()
│   │   └── roles.py              # require_role(), require_any_role()
│   ├── core/
│   │   ├── __init__.py
│   │   ├── vehicle.py            # Vehicle (threading.Thread, daemon)
│   │   ├── traffic_light.py      # TrafficLight (threading.Semaphore)
│   │   ├── scheduler.py          # TrafficScheduler (queue.PriorityQueue)
│   │   ├── intersection.py       # Intersection (nodo de red)
│   │   ├── deadlock_detector.py  # DeadlockDetector (timeout 10s)
│   │   └── fault_handler.py      # FaultHandler (thread demon, 15-30s)
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py           # Engine, SessionLocal, Base, get_db()
│   │   └── models.py             # User, EventLog, LightConfig
│   ├── simulation/
│   │   ├── __init__.py
│   │   ├── engine.py             # SimulationEngine (_loop tick=1s)
│   │   └── network.py             # IntersectionNetwork (RAG)
│   ├── main.py                    # FastAPI app, lifespan, CORS, routers
│   ├── config.py                  # Settings (Pydantic), constantes
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx                # Componente principal (scaffold Vite)
│   │   ├── components/            # Componentes UI (pendiente impl)
│   │   ├── hooks/                 # Custom hooks (pendiente impl)
│   │   └── services/              # API service (pendiente impl)
│   ├── package.json
│   ├── vite.config.js
│   ├── eslint.config.js
│   └── tailwind.config.js
├── docs/
│   └── ENTREGA_1/
│       └── 02_ARQUITECTURA.md     # Este documento
├── .gitignore
├── README.md
├── AGENTS.md
├── ENTREGA_1.md
└── ENTREGA_2.md
```

---

## 11. CICLO DE VIDA DE LA SIMULACIÓN

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         CICLO DE VIDA DE LA SIMULACIÓN                   │
└──────────────────────────────────────────────────────────────────────────┘

1. INICIALIZACIÓN (Startup)
   ├── POST /simulation/start
   ├── Crear IntersectionNetwork (3x3 grid → 9 nodos)
   ├── Conectar nodos (arriba-abajo, izquierda-derecha)
   ├── Crear TrafficScheduler
   ├── Crear SimulationEngine
   └── Iniciar FaultHandler (thread demon)

2. EJECUCIÓN (Running)
   │
   ├── SimulationEngine._loop() [cada 1s]
   │   ├── Para cada intersección:
   │   │   ├── Verificar estado actual (RED|GREEN|YELLOW|FAULT)
   │   │   ├── Si FAULT → ignorar transición
   │   │   ├── Actualizar timer interno
   │   │   └── Transicionar: RED→GREEN→YELLOW→RED
   │   │       └── En GREEN: scheduler.dispatch_next()
   │   │
   │   └── time.sleep(1.0)

   ├── FaultHandler._fault_loop() [cada 15-30s aleatorio]
   │   ├── Seleccionar intersección aleatoria
   │   ├── light.trigger_fault() → estado = "FAULT"
   │   ├── Broadcast FAULT via WebSocket
   │   ├── time.sleep(5s) [auto-recuperación]
   │   └── light.restore() → estado = "RED"
   │       └── Broadcast RESTORE via WebSocket

   └── DeadlockDetector._check_loop() [cada 1s]
       ├── Verificar timestamps de vehículos en cola
       └── Si timeout > 10s → on_deadlock() → EventLog

3. TERMINACIÓN (Shutdown)
   ├── POST /simulation/stop
   ├── engine.stop() → _stop_event.set()
   ├── FaultHandler.stop()
   ├── DeadlockDetector.stop()
   └── Limpiar variables globales (_engine = None)
```

---

## 12. MODELO DE CONCURRENCIA

### 12.1 Hilos Activos en el Sistema

| Hilo | Tipo | Origen | Frecuencia | Propósito |
|------|------|--------|------------|-----------|
| SimulationEngine._loop | Daemon | engine.start() | 1 Hz | Kernel tick - gestión de estados |
| FaultHandler._fault_loop | Daemon | fault_handler.start() | 15-30s | Generación de faults |
| DeadlockDetector._check_loop | Daemon | deadlock_detector.start() | 1 Hz | Detección de interbloqueos |
| Vehicle (N instancias) | Daemon | engine.add_vehicle() | Por vehículo | Simular vehículo individual |

### 12.2 Mecanismos de Sincronización

| Mecanismo | Clase | Uso |
|-----------|-------|-----|
| `threading.Semaphore(1)` | TrafficLight | Exclusión mutua en intersección |
| `threading.Lock` | TrafficLight | Proteger lectura/escritura de estado |
| `threading.Event` | TrafficLight | Señalización de fault |
| `threading.Event` | Vehicle | Dispatch signal del scheduler |
| `queue.PriorityQueue` | TrafficScheduler | Ready queue con prioridad |

### 12.3 Estados de un Vehículo (Vehicle)

```
     ┌─────────────────────────────────────────────────────────┐
     │                                                         │
     │  ┌──────────┐    scheduler.enqueue()    ┌──────────┐   │
     │  │          │ ───────────────────────> │          │   │
     │  │   NEW    │                          │  WAITING │   │
     │  │          │                          │          │   │
     │  └──────────┘                          └─────┬────┘   │
     │                                              │         │
     │                                              │ scheduler│
     │                                              │.wait_for│
     │                                              │_dispatch│
     │                                              │         │
     │  ┌──────────┐    current_position++          │         │
     │  │          │ <─────────────────────────────┼─────────┤
     │  │  MOVING  │                                │         │
     │  │          │ ───────────────────────>       │         │
     │  └──────────┘    (siguiente intersección)   │         │
     │                                              │         │
     │  ┌──────────┐    route completada           │         │
     │  │          │ <─────────────────────────────┼─────────┤
     │  │   DONE    │                               │         │
     │  │          │                               │         │
     │  └──────────┘                               │         │
     │                                              │         │
     │  ┌──────────┐    timeout 10s (Deadlock)    │         │
     │  │          │ <─────────────────────────────┼─────────┤
     │  │ BLOCKED  │                               │         │
     │  │          │                               │         │
     │  └──────────┘                               │         │
     │                                              │         │
     └──────────────────────────────────────────────┴─────────┘
```

---

## 13. CONFIGURACIÓN DEL SISTEMA

### 13.1 Constantes de Simulación

| Constante | Valor | Descripción |
|-----------|-------|-------------|
| `SIMULATION_TICK_INTERVAL` | 1.0s | Intervalo del kernel tick |
| `FAULT_MIN_INTERVAL` | 15s | Mínimo entre faults |
| `FAULT_MAX_INTERVAL` | 30s | Máximo entre faults |
| `FAULT_RECOVERY_TIME` | 5s | Tiempo de auto-recuperación |
| `TRAFFIC_LIGHT_DEFAULT_GREEN` | 10s | Tiempo verde por defecto |
| `TRAFFIC_LIGHT_DEFAULT_RED` | 10s | Tiempo rojo por defecto |
| `TRAFFIC_LIGHT_YELLOW_DURATION` | 3s | Duración del amarillo |
| `DEADLOCK_TIMEOUT` | 10s | Timeout para detectar deadlock |

### 13.2 Grid de Intersecciones (3x3)

```
       j=0         j=1         j=2
    ┌─────────┐  ┌─────────┐  ┌─────────┐
i=0 │intersec_│  │intersec_│  │intersec_│
    │  _0_0   │  │  _0_1   │  │  _0_2   │
    └────┬────┘  └────┬────┘  └────┬────┘
         │           │           │
         │           │           │
    ┌────┴────┐  ┌────┴────┐  ┌────┴────┐
i=1 │intersec_│  │intersec_│  │intersec_│
    │  _1_0   │  │  _1_1   │  │  _1_2   │
    └────┬────┘  └────┬────┘  └────┬────┘
         │           │           │
         │           │           │
    ┌────┴────┐  ┌────┴────┐  ┌────┴────┐
i=2 │intersec_│  │intersec_│  │intersec_│
    │  _2_0   │  │  _2_1   │  │  _2_2   │
    └─────────┘  └─────────┘  └─────────┘
```

### 13.3 Prioridades de Vehículos

| Prioridad | Valor Enum | Descripción |
|-----------|------------|-------------|
| EMERGENCY | 0 | Ambulancias, bomberos (máxima prioridad) |
| HIGH | 1 | Transporte público |
| NORMAL | 2 | Tráfico particular regular |

---

**IMPORTANTE:** Este documento refleja la arquitectura completa del sistema para ENTREGA 1. Cualquier modificación a la estructura de módulos, clases o flujos debe actualizarse en este documento.
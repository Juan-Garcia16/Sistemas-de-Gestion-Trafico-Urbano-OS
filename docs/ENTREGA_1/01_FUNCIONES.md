# Dokumentación de Funciones - ENTREGA 1
## Sistema de Gestión de Tráfico Urbano

```markdown
# FUNCIONES POR MÓDULO

## 1. backend/config.py

| Función/Clase | Tipo | Parámetros | Retorna | Descripción |
|----------------|------|------------|---------|-------------|
| Settings | Clase | - | BaseModel | Configuración global validada con Pydantic |

**Atributos de Settings:**
- BASE_DIR: Path
- DB_PATH: str
- JWT_SECRET: str
- JWT_ALGORITHM: str = "HS256"
- JWT_EXPIRATION_HOURS: int = 8
- SIMULATION_TICK_INTERVAL: float = 1.0
- FAULT_MIN_INTERVAL: int = 15
- FAULT_MAX_INTERVAL: int = 30
- FAULT_RECOVERY_TIME: int = 5
- TRAFFIC_LIGHT_DEFAULT_GREEN: int = 10
- TRAFFIC_LIGHT_DEFAULT_RED: int = 10
- TRAFFIC_LIGHT_YELLOW_DURATION: int = 3
- API_HOST: str = "0.0.0.0"
- API_PORT: int = 8000

---

## 2. backend/db/database.py

| Función/Variable | Tipo | Descripción |
|-------------------|------|-------------|
| engine | Variable | create_engine SQLite con check_same_thread=False |
| SessionLocal | Variable | sessionmaker para crear sesiones |
| Base | Variable | declarative_base para modelos ORM |
| get_db() | Función | Dependency de FastAPI para obtener sesión DB |

---

## 3. backend/db/models.py

| Clase | Tabla | Atributos | Descripción |
|-------|-------|-----------|-------------|
| User | users | id, username, password_hash, role | Usuario para autenticación |
| EventLog | event_log | id, timestamp, event_type, intersection_id, vehicle_id, details, user_id | Log de auditoría |
| LightConfig | light_config | intersection_id, green_time, red_time, updated_by, updated_at | Configuración de semáforos |

---

## 4. backend/auth/jwt_handler.py

| Función | Parámetros | Retorna | Descripción |
|---------|------------|---------|-------------|
| create_token | user_id: str, role: str | str | Crea JWT con payload {sub, role, exp} |
| decode_token | token: str | dict | Decodifica y valida JWT |
| get_current_user | token: str = Depends(oauth2_scheme) | dict | Dependencia FastAPI para usuario actual |

---

## 5. backend/auth/roles.py

| Función | Parámetros | Retorna | Descripción |
|---------|------------|---------|-------------|
| require_role | required_role: str | Depends | Decorador para proteger rutas por rol |
| require_any_role | *roles | Depends | Acepta cualquiera de los roles dados |
| get_optional_user | - | dict\|None | Retorna usuario sin requerir auth |

**Constantes:**
- ROLES: list = ["viewer", "control"]

---

## 6. backend/api/websocket.py

| Clase/Método | Parámetros | Retorna | Descripción |
|--------------|------------|---------|-------------|
| ConnectionManager | - | - | Gestor de conexiones WebSocket |
| .connect() | ws: WebSocket | - | Acepta y registra conexión |
| .disconnect() | ws: WebSocket | - | Remueve conexión |
| .broadcast() | data: dict | - | Envía a todos los clientes |
| .send_personal() | ws: WebSocket, data: dict | - | Envía a cliente específico |
| manager | Instancia | ConnectionManager | Instancia global |
| websocket_endpoint | ws: WebSocket | - | Endpoint /ws |

---

## 7. backend/api/routes_auth.py

| Función | Endpoint | Auth | Descripción |
|---------|----------|------|-------------|
| register | POST /auth/register | No | Registra usuario con bcrypt |
| login | POST /auth/login | No | Login OAuth2, retorna JWT |

**Modelos:**
- RegisterRequest: username, password, role

**Helpers:**
- verify_password(plain_password, hashed_password) -> bool
- get_password_hash(password) -> str

---

## 8. backend/api/routes_simulation.py

| Función | Endpoint | Rol | Descripción |
|---------|----------|-----|-------------|
| start_simulation | POST /simulation/start | control | Crea engine, network, fault handler |
| stop_simulation | POST /simulation/stop | control | Detiene simulación |
| get_status | GET /simulation/status | viewer/control | Retorna snapshot del estado |
| add_vehicle | POST /simulation/vehicle | control | Agrega vehículo |

**Modelos:**
- AddVehicleRequest: id, route, priority

**Variables globales:**
- _engine: SimulationEngine | None
- _network: IntersectionNetwork | None
- _scheduler: TrafficScheduler | None

---

## 9. backend/api/routes_control.py

| Función | Endpoint | Rol | Descripción |
|---------|----------|-----|-------------|
| update_timing | PUT /control/lights/:id/timing | control | Actualiza tiempos semáforo |
| trigger_fault | POST /control/lights/:id/fault | control | Simula fallo manual |
| get_lights | GET /control/lights | control | Lista configuración |
| get_logs | GET /logs | control | Obtiene eventos |

**Modelos:**
- UpdateTimingRequest: green_time, red_time

---

## 10. backend/core/traffic_light.py

| Clase/Método | Descripción |
|--------------|-------------|
| TrafficLight | Semáforo como recurso compartido (Mutex) |
| .__init__(intersection_id, green_time) | Inicializa mutex, lock, fault_event |
| .acquire(vehicle_id, timeout) | P() - Wait() - adquiere el semáforo |
| .release() | V() - Signal() - libera el semáforo |
| .trigger_fault() | Inyecta interrupción (cambia a FAULT) |
| .restore() | ISR -恢复了 operativa normal |

**Atributos:**
- id: str
- state: str (RED|GREEN|YELLOW|FAULT)
- green_time: int
- semaphore: Semaphore(1) - mutex
- fault_event: Event -模拟中断
- _lock: Lock - proteger estado

---

## 11. backend/core/vehicle.py

| Clase/Enum | Descripción |
|------------|-------------|
| Priority(IntEnum) | EMERGENCY=0, HIGH=1, NORMAL=2 |
| Vehicle(threading.Thread) | Proceso individual (daemon) |

**Métodos de Vehicle:**
| Método | Descripción |
|--------|-------------|
| .__init__(vehicle_id, route, priority, scheduler) | Inicializa PCB |
| .run() | Ciclo de vida del proceso |

**Atributos de Vehicle:**
- vehicle_id: str
- route: list
- priority: Priority
- scheduler: TrafficScheduler
- current_position: int
- status: str (WAITING|MOVING|DONE)

---

## 12. backend/core/scheduler.py

| Clase | Descripción |
|-------|-------------|
| TrafficScheduler | Planificador de Priority Scheduling |

| Método | Descripción |
|--------|-------------|
| .__init__() | Inicializa colas y eventos |
| .enqueue(vehicle, intersection_id) | Encola proceso en ready queue |
| .dispatch_next(intersection_id) | Dispatcher - otorga recurso |
| .wait_for_dispatch(vehicle_id) | Bloquea hasta dispatch |

**Atributos:**
- _queues: dict[str, PriorityQueue]
- _dispatch_events: dict[str, threading.Event]
- _lock: Lock

---

## 13. backend/core/intersection.py

| Clase | Descripción |
|-------|-------------|
| Intersection | Nodo de la red de tráfico |

| Propiedad | Retorna | Descripción |
|-----------|---------|-------------|
| .id | str | Identificador de la intersección |
| .state | str | Estado del semáforo |
| .light | TrafficLight | Recurso incrustado |

---

## 14. backend/core/fault_handler.py

| Método | Descripción |
|--------|-------------|
| FaultHandler.__init__(network, on_fault, on_restore) | Inicializa con callbacks |
| .start() | Inicia thread demonio |
| .stop() | Detiene handler |
| ._fault_loop() | Loop que genera fallos cada 15-30s |

**Parámetros:**
- network: IntersectionNetwork
- on_fault: callback(intersection_id)
- on_restore: callback(intersection_id)

**Atributos:**
- _running: bool
- _thread: Thread

---

## 15. backend/core/deadlock_detector.py

| Método | Descripción |
|--------|-------------|
| DeadlockDetector.__init__(scheduler, on_deadlock) | Inicializa |
| .start() | Inicia thread demonio |
| .stop() | Detiene detector |
| .register_vehicle(vehicle_id) | Registra timestamp |
| .unregister_vehicle(vehicle_id) | Remueve vehículo |
| ._check_loop() | Verifica timeout cada 1s |

**Constantes:**
- MAX_WAIT_TIME: int = 10

**Atributos:**
- scheduler: TrafficScheduler
- on_deadlock: callback(vehicle_id, intersection_id)
- _vehicle_timestamps: dict[str, float]
- _running: bool
- _thread: Thread

---

## 16. backend/simulation/network.py

| Clase | Descripción |
|-------|-------------|
| IntersectionNetwork | Grafo de recursos (RAG) |

| Método | Descripción |
|--------|-------------|
| .__init__() | Inicializa nodos y adyacencia |
| .add_intersection(intersection_id) | Añade nodo |
| .connect(id1, id2, bidirectional) | Conecta nodos |
| .get_neighbors(intersection_id) | Retorna adyacentes |
| .get_all() | Retorna todos los nodos |

**Atributos:**
- nodes: dict[str, Intersection]
- adjacency_list: dict[str, list[str]]

---

## 17. backend/simulation/engine.py

| Clase | Descripción |
|-------|-------------|
| SimulationEngine | Motor central (Kernel tick loop) |

| Método | Descripción |
|--------|-------------|
| .__init__(network, scheduler) | Inicializa engine |
| .start() | Inicia thread del kernel |
| .stop() | Detiene simulación |
| ._loop() | Tick loop principal |
| .add_vehicle(vehicle_id, route, priority) | Crea proceso |
| .state_snapshot() | Retorna estado actual |

**Atributos:**
- network: IntersectionNetwork
- scheduler: TrafficScheduler
- active_vehicles: dict[str, Vehicle]
- _light_timers: dict[str, int]
- _stop_event: Event
- _tick_thread: Thread

---

## 18. backend/main.py

| Función/Variable | Descripción |
|------------------|-------------|
| lifespan(app) | Crea tablas DB en startup |
| app | FastAPI con lifespan, CORS, routers |
| root() | GET / → {status, system} |
| health_check() | GET /health → {status: healthy} |

**Routers incluidos:**
- auth_router (prefix: /auth)
- simulation_router (prefix: /simulation)
- control_router (prefix: /control)
- websocket_router (prefix: /ws)

**Middlewares:**
- CORSMiddleware (allow_origins=*)

---

# FRONTEND

## 19. frontend/src/hooks/useWebSocket.js

| Hook/Función | Parámetros | Retorna | Descripción |
|--------------|------------|---------|-------------|
| useWebSocket() | - | state | Hook para WebSocket con auto-reconnect |

**state retornado:**
```javascript
{
  intersections: [],  // lista de intersecciones
  vehicles: [],       // lista de vehículos
  alerts: [],        // alertas FAULT/EMERGENCY
  connected: false,  // estado de conexión
  error: null        // mensaje de error
}
```

**Constantes:**
- WS_URL: string = import.meta.env.VITE_WS_URL || "ws://localhost:8000/ws"

**Métodos internos:**
- connect(): Establece conexión WebSocket
- Auto-reconnect: 2 segundos al desconectarse

**Manejo de mensajes:**
- STATE_UPDATE: Actualiza intersections, vehicles, alerts
- FAULT: Añade alerta de fallo
- EMERGENCY: Añade alerta de emergencia

---

## 20. frontend/src/services/api.js

| Clase | Descripción |
|-------|-------------|
| ApiService | Cliente API REST |

| Método | Endpoint | Auth | Descripción |
|--------|----------|------|-------------|
| login(username, pwd) | POST /auth/login | No | Login con FormData |
| register(user, pwd, role) | POST /auth/register | No | Registro |
| startSimulation() | POST /simulation/start | Sí | Inicia simulación |
| stopSimulation() | POST /simulation/stop | Sí | Detiene simulación |
| getStatus() | GET /simulation/status | Sí | Estado actual |
| addVehicle(id, route, priority) | POST /simulation/vehicle | Sí | Agrega vehículo |
| updateLightTiming(id, green, red) | PUT /control/lights/:id/timing | Sí | Actualiza config |
| triggerFault(id) | POST /control/lights/:id/fault | Sí | Trigger fallo |
| getLogs(type, limit) | GET /logs | Sí | Obtiene logs |

**Constantes:**
- API_BASE: string = import.meta.env.VITE_API_URL || "http://localhost:8000"

**Métodos internos:**
- setToken(token): Almacena/elimina token
- request(method, path, body, requiresAuth): Ejecuta fetch

**Almacenamiento:**
- Token en localStorage
- Rol en localStorage

---

## 21. frontend/src/components/LoginForm.jsx

| Componente | Props | Descripción |
|------------|-------|-------------|
| LoginForm | onLogin: function | Formulario de login |

**Estado interno:**
- username: string
- password: string
- error: string
- loading: boolean

**Métodos:**
- handleSubmit(e): Procesa login con api.login()

---

## 22. frontend/src/components/AlertBanner.jsx

| Componente | Props | Descripción |
|------------|-------|-------------|
| AlertBanner | alerts: array | Banner de alertas en tiempo real |

**Estado interno:**
- dismissed: array (timestamps descartados)

**Tipos de alerta:**
- FAULT: Fallo en intersección (rojo)
- EMERGENCY: Vehículo de emergencia (amarillo)

---

## 23. frontend/src/App.jsx

| Función | Descripción |
|---------|-------------|
| App | Componente principal |
| handleLogin(role) | Callback post-login |
| handleLogout() | Limpia sesión |
| handleStartSimulation() | Inicia simulación |
| handleStopSimulation() | Detiene simulación |

**Estado:**
- user: string | null (desde localStorage)
- simulationRunning: boolean
- wsState: object (useWebSocket)

**Renders:**
- LoginForm si no hay usuario
- Dashboard completo si autenticado

**Dashboard incluye:**
- Header con estado de conexión y rol
- Control de simulación (iniciar/detener)
- Grid de intersecciones (estado visual)
- Lista de vehículos (estado, prioridad, ruta)

---

# RESUMEN DE IMPORT/EXPORT

## Dependencias Backend

```
config.py
  └→ (sin deps externas)
  └→ exporta: settings, BASE_DIR, DB_PATH, JWT_SECRET, JWT_ALGORITHM,
              JWT_EXPIRATION_HOURS, SIMULATION_TICK_INTERVAL,
              FAULT_MIN_INTERVAL, FAULT_MAX_INTERVAL, FAULT_RECOVERY_TIME,
              TRAFFIC_LIGHT_DEFAULT_GREEN, TRAFFIC_LIGHT_DEFAULT_RED,
              TRAFFIC_LIGHT_YELLOW_DURATION, API_HOST, API_PORT

db/database.py
  └→ importa: config.DB_PATH
  └→ exporta: engine, SessionLocal, Base, get_db

db/models.py
  └→ importa: sqlalchemy.Column, Integer, String, Text, db.database.Base
  └→ exporta: User, EventLog, LightConfig

auth/jwt_handler.py
  └→ importa: config (JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRATION_HOURS),
             fastapi (Depends, HTTPException), fastapi.security (OAuth2PasswordBearer),
             jose (JWTError, jwt)
  └→ exporta: oauth2_scheme, create_token, decode_token, get_current_user

auth/roles.py
  └→ importa: fastapi (Depends, HTTPException), jose (JWTError),
             auth.jwt_handler (oauth2_scheme, decode_token)
  └→ exporta: ROLES, require_role, require_any_role, get_optional_user

api/websocket.py
  └→ importa: fastapi (WebSocket, WebSocketDisconnect, APIRouter),
             json, auth.jwt_handler.decode_token
  └→ exporta: ConnectionManager, manager, websocket_endpoint, router

api/routes_auth.py
  └→ importa: fastapi (APIRouter, Depends, HTTPException, status),
             fastapi.security (OAuth2PasswordRequestForm),
             passlib.context (CryptContext),
             pydantic (BaseModel),
             sqlalchemy.orm (Session),
             uuid, db.database (get_db), db.models (User),
             auth.jwt_handler (create_token)
  └→ exporta: router, verify_password, get_password_hash

api/routes_simulation.py
  └→ importa: fastapi (APIRouter, Depends, HTTPException),
             sqlalchemy.orm (Session), pydantic (BaseModel), uuid,
             auth.roles (require_role),
             core.vehicle (Priority),
             simulation.engine (SimulationEngine),
             simulation.network (IntersectionNetwork),
             core.scheduler (TrafficScheduler),
             api.websocket (manager)
  └→ exporta: router, get_engine

api/routes_control.py
  └→ importa: fastapi (APIRouter, Depends, HTTPException),
             sqlalchemy.orm (Session), pydantic (BaseModel), datetime,
             auth.roles (require_role),
             db.database (get_db), db.models (EventLog, LightConfig),
             api.routes_simulation (get_engine)
  └→ exporta: router

core/traffic_light.py
  └→ importa: threading (Semaphore, Event, Lock), time
  └→ exporta: TrafficLight

core/vehicle.py
  └→ importa: threading.Thread, enum.IntEnum
  └→ exporta: Priority, Vehicle

core/scheduler.py
  └→ importa: queue, threading, time
  └→ exporta: TrafficScheduler

core/intersection.py
  └→ importa: core.traffic_light (TrafficLight)
  └→ exporta: Intersection

core/fault_handler.py
  └→ importa: threading, random, time, typing.Callable, config, simulation.network
  └→ exporta: FaultHandler

core/deadlock_detector.py
  └→ importa: threading, time, typing.Callable, simulation.network, core.scheduler
  └→ exporta: DeadlockDetector

simulation/network.py
  └→ importa: core.intersection (Intersection)
  └→ exporta: IntersectionNetwork

simulation/engine.py
  └→ importa: threading, time, simulation.network, core.scheduler, core.vehicle
  └→ exporta: SimulationEngine

main.py
  └→ importa: contextlib (asynccontextmanager),
             fastapi (FastAPI, WebSocket),
             fastapi.middleware.cors (CORSMiddleware),
             api.routes_auth, api.routes_simulation, api.routes_control,
             api.websocket, db.database, core.traffic_light, core.vehicle,
             core.scheduler, core.intersection, simulation.engine, simulation.network
  └→ exporta: app, root, health_check
```

## Dependencias Frontend

```
hooks/useWebSocket.js
  └→ importa: react (useEffect, useState, useRef, useCallback)
  └→ exporta: useWebSocket

services/api.js
  └→ importa: (ninguno - usa fetch nativo)
  └→ exporta: api (ApiService instance)

components/LoginForm.jsx
  └→ importa: react (useState), ../services/api
  └→ exporta: LoginForm

components/AlertBanner.jsx
  └→ importa: react (useState)
  └→ exporta: AlertBanner

App.jsx
  └→ importa: react (useState), ./components/LoginForm,
             ./components/AlertBanner, ./hooks/useWebSocket, ./services/api
  └→ exporta: App (default)
```

---

# MAPA DE CONCEPTOS SO → CÓDIGO

| Concepto de SO | Implementación en código |
|---------------|------------------------|
| Proceso/Hilo | Vehicle(threading.Thread) con daemon=True |
| PCB (Process Control Block) | Atributos de Vehicle: vehicle_id, status, priority, route |
| Scheduler/CPU Scheduler | TrafficScheduler - PriorityQueue por intersección |
| Priority Scheduling | Priority(IntEnum): EMERGENCY=0, HIGH=1, NORMAL=2 |
| Dispatcher | scheduler.dispatch_next() → threading.Event.set() |
| Wait/Block | scheduler.wait_for_dispatch() → event.wait() |
| Context Switch | Threading.Event醒来 Vehicle de wait_for_dispatch |
| Semaphore (Mutex) | TrafficLight.semaphore = Semaphore(1) |
| P() / Wait() | TrafficLight.acquire() |
| V() / Signal() | TrafficLight.release() |
| Sección Crítica | Recursos protegidos por TrafficLight._lock |
| Deadlock Detection | DeadlockDetector con MAX_WAIT_TIME=10s |
| Deadlock Resolution | Remover vehículo de cola (rollback) |
| Interrupción | TrafficLight.fault_event (threading.Event) |
| ISR (Interrupt Service Routine) | TrafficLight.restore() |
| Kernel Tick Loop | SimulationEngine._loop() cada 1s |
| Resource Allocation Graph (RAG) | IntersectionNetwork (nodes + adjacency_list) |
| Interrupt Fault Handler | FaultHandler._fault_loop() cada 15-30s |
| Auto-recovery | FaultHandler con FAULT_RECOVERY_TIME=5s |
| JWT Authentication | auth/jwt_handler.py - create_token, decode_token |
| Role-Based Access | auth/roles.py - require_role, require_any_role |
| WebSocket Broadcast | ConnectionManager.broadcast() |
```

---

**Documento generado para ENTREGA_1 - Sistema de Gestión de Tráfico Urbano**
**Versión: 1.0.0**
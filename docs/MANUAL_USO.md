# Manual de Usuario — Sistema de Gestión de Tráfico Urbano

Sistema académico que modela una red de intersecciones urbanas con vehículos concurrentes, semáforos sincronizados, prioridad para emergencias, detección de fallos y control de acceso por roles.

**Stack:** Python/FastAPI (threading) · React 19 + Vite + TailwindCSS v4 · SQLite · WebSocket

---

## 1. Requisitos e Instalación

### 1.1 Requisitos previos

- Python 3.11+
- Node.js 18+
- Navegador web moderno (Firefox, Chrome)

### 1.2 Instalación y Arranque

**Backend:**

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend (en otra terminal):**

```bash
cd frontend
npm install
npm run dev
```

### 1.3 URLs de Acceso

| Servicio | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Swagger Docs | http://localhost:8000/docs |

---

## 2. Credenciales de Prueba

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| admin | admin123 | control |
| ctrl | pass | control |
| viewer1 | pass | viewer |

---

## 3. Roles de Usuario

| Rol | Permisos |
|-----|----------|
| **viewer** | Solo ver estado de la simulación |
| **control** | Iniciar/detener simulación, modificar semáforos, ver logs |

---

## 4. Guía de Uso

### 4.1 Registro y Login

1. Abrir http://localhost:5173
2. El sistema permite registro directo o login con las credenciales de prueba
3. Tras autenticarse, se muestra el dashboard principal

### 4.2 Iniciar Simulación

1. Iniciar sesión con rol **control**
2. Hacer clic en **"Iniciar Simulación"**
3. El sistema crea automáticamente una red de **3×3 intersecciones** (9 nodos)
4. Las intersecciones aparecen en el panel central
5. Se inyectan vehículos automáticos que cruzan la red

### 4.3 Detener Simulación

1. Hacer clic en **"Detener Simulación"**
2. Todos los vehículos se detienen y la red queda inactiva

### 4.4 Agregar Vehículo

**Desde el panel de control (rol control):**

1. Hacer clic en **"+ Emergencia"** para agregar un vehículo de emergencia con prioridad máxima
2. O usar el endpoint API directamente:

```bash
curl -X POST http://localhost:8000/simulation/vehicle \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"id": "vehicle_1", "route": ["intersection_0_0", "intersection_0_1"], "priority": "EMERGENCY"}'
```

### 4.5 Modificar Tiempos de Semáforo

1. Seleccionar una intersección del menú desplegable
2. Ajustar los sliders de **Verde** y **Rojo** (rango: 3-30 segundos)
3. Hacer clic en **"Actualizar Tiempos"**

### 4.6 Simular Fallo Manual

1. En el panel **"Simular Fallo"**, hacer clic en el botón correspondiente a la intersección
2. El semáforo parará su ciclo normal y mostrará estado `FAULT` (gris con parpadeo)
3. Se auto-recupera tras **5 segundos**

### 4.7 Ver Logs de Eventos

1. Acceder a **"Ver Logs"** desde el panel de control
2. Se muestra un historial de eventos: fallos, cambios de configuración, emergencias

---

## 5. Endpoints de la API

### 5.1 Autenticación

| Método | Endpoint | Auth | Descripción |
|--------|----------|------|-------------|
| `POST` | `/auth/register` | No | Registro de usuario |
| `POST` | `/auth/login` | No | Login (FormData OAuth2) → JWT |

**Ejemplo de registro:**

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "test123", "role": "viewer"}'
```

**Ejemplo de login:**

```bash
curl -X POST http://localhost:8000/auth/login \
  -F "username=admin" \
  -F "password=admin123"
```

**Respuesta de login:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "role": "control"
}
```

### 5.2 Simulación

| Método | Endpoint | Rol | Descripción |
|--------|----------|-----|-------------|
| `POST` | `/simulation/start` | control | Iniciar simulación (grid 3×3) |
| `POST` | `/simulation/stop` | control | Detener simulación |
| `GET` | `/simulation/status` | viewer/control | Estado actual |
| `POST` | `/simulation/vehicle` | control | Agregar vehículo |

**Ejemplo de estado:**

```json
{
  "running": true,
  "tick": 42,
  "intersections": [
    {"id": "intersection_0_0", "state": "GREEN", "position": {"x": 0, "y": 0}},
    {"id": "intersection_0_1", "state": "YELLOW", "position": {"x": 1, "y": 0}}
  ],
  "vehicles": [
    {"id": "v1", "status": "MOVING", "position": 1, "priority": "NORMAL"}
  ]
}
```

### 5.3 Control

| Método | Endpoint | Rol | Descripción |
|--------|----------|-----|-------------|
| `PUT` | `/control/lights/:id/timing` | control | Actualizar tiempos |
| `POST` | `/control/lights/:id/fault` | control | Trigger fault manual |
| `GET` | `/control/lights` | control | Lista configuraciones |
| `GET` | `/logs` | control | Obtener logs |

**Ejemplo de actualización de tiempos:**

```bash
curl -X PUT "http://localhost:8000/control/lights/intersection_0_0/timing?green_time=15&red_time=15" \
  -H "Authorization: Bearer <token>"
```

### 5.4 WebSocket

| Endpoint | Auth | Descripción |
|----------|------|-------------|
| `WS` | No | Broadcast de estado en tiempo real |

**URL:** `ws://localhost:8000/ws`

**Tipos de mensajes entrantes:**

```json
// STATE_UPDATE (cada 1 segundo)
{
  "type": "STATE_UPDATE",
  "intersections": [
    {"id": "intersection_0_0", "state": "GREEN"}
  ],
  "vehicles": [
    {"id": "v1", "status": "MOVING", "position": 1}
  ],
  "alerts": [],
  "timestamp": "2026-05-14T10:30:00Z"
}

// FAULT
{
  "type": "FAULT",
  "intersection_id": "intersection_0_1",
  "timestamp": "2026-05-14T10:30:00Z"
}

// EMERGENCY
{
  "type": "EMERGENCY",
  "vehicle_id": "emergency_1",
  "timestamp": "2026-05-14T10:30:00Z"
}
```

---

## 6. Estados de los Semáforos

| Estado | Color | Descripción |
|--------|-------|-------------|
| `RED` | Rojo | Semáforo en rojo — vehículos deben esperar |
| `GREEN` | Verde | Semáforo en verde — vehículos pueden cruzar |
| `YELLOW` | Amarillo | Transición — próximo a rojo |
| `FAULT` | Gris (parpadeo) | Fallo detectado — auto-recuperación en 5s |

### Ciclo de transición (sin faults):

```
RED → GREEN → YELLOW → RED
      ↑________________|
```

- Tiempo en verde: configurable (por defecto 10s)
- Tiempo en amarillo: 3s
- Tiempo en rojo: igual al tiempo en verde

---

## 7. Estados de los Vehículos

| Estado | Descripción |
|--------|-------------|
| `WAITING` | Encolado, esperando su turno en la intersección |
| `MOVING` | Cruzando la intersección |
| `DONE` | Ruta completada |
| `BLOCKED` | Timeout detectado por DeadlockDetector (10s) |

---

## 8. Prioridades de Vehículos

| Prioridad | Valor | Uso |
|-----------|-------|-----|
| `EMERGENCY` | 0 | Ambulancias, bomberos — máxima prioridad |
| `HIGH` | 1 | Transporte público |
| `NORMAL` | 2 | Tráfico regular |

Los vehículos de mayor prioridad son despachados primero por el `TrafficScheduler` en cada intersección.

---

## 9. Fallos Automáticos (FaultHandler)

El sistema inyecta fallos aleatorios cada **15-30 segundos**:

1. Selecciona una intersección al azar
2. Su semáforo pasa a estado `FAULT`
3. Se notifica vía WebSocket al frontend
4. Se auto-recupera tras **5 segundos** (vuelve a `RED`)

Esto simula el concepto de **interrupción de hardware** en un sistema operativo.

---

## 10. Detección de Deadlock

El `DeadlockDetector` monitoriza vehículos que esperan más de **10 segundos** sin ser despachados:

1. Si un vehículo supera el timeout, se marca como `BLOCKED`
2. Se registra el evento en la base de datos (`event_log`)
3. El vehículo es removido de la cola de espera

---

## 11. Mapeo de Conceptos de Sistemas Operativos

| Concepto SO | Implementación |
|-------------|----------------|
| Proceso/Hilo | `Vehicle` → `threading.Thread` (daemon) |
| Semáforo (Mutex) | `TrafficLight.semaphore` → `threading.Semaphore(1)` |
| Priority Scheduling | `TrafficScheduler` → `queue.PriorityQueue` |
| Interrupción | `TrafficLight.fault_event` → `threading.Event` |
| ISR (recuperación) | `TrafficLight.restore()` |
| Kernel Tick | `SimulationEngine._loop()` cada 1s |
| Deadlock Detection | `DeadlockDetector` con timeout 10s |
| Roles JWT | `viewer` (solo lectura) / `control` (escritura) |

---

## 12. Limitaciones de la Versión Actual

- El frontend visual muestra un **grid simple** con tarjetas de estado
- Los componentes `IntersectionGrid`, `TrafficLight`, `VehicleMarker` y `ControlPanel` están **pendientes de implementar** como componentes visuales completos (grid interactivo con animaciones)
- La documentación de funciones y arquitectura detallada se encuentra en `docs/ENTREGA_1/`

---

**Versión del documento:** 1.0
**Última actualización:** Mayo 2026
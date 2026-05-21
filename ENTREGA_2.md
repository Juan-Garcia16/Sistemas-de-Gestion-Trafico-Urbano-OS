# ENTREGA 2: Integración Completa — Backend + Frontend End-to-End

## Objetivo de la Entrega
Sistema funcional end-to-end: frontend visual con grid de intersecciones, semáforos animados, vehículos en movimiento, panel de control y login. Backend con FaultHandler y DeadlockDetector conectados, datos de vehículos completos, y broadcast en tiempo real de todos los eventos del sistema.

## Dependencias de la Entrega 1
- Backend completo con API REST y WebSocket
- Frontend con hooks/useWebSocket.js y services/api.js
- LoginForm.jsx y AlertBanner.jsx funcionando

---

## Tarea 17: `frontend/src/components/TrafficLight.jsx` — Semáforo Visual

**Archivo a crear:** `frontend/src/components/TrafficLight.jsx`

**Descripción:**
Componente visual que representa un semáforo con colores según su estado actual.

**Props:**
```javascript
{
  id: string,           // identificador de la intersección
  state: "RED" | "GREEN" | "YELLOW" | "FAULT",
  position: { x: number, y: number }  // posición en el grid
}
```

**Requisitos visuales:**
- Círculo de 40-50px con color según estado:
  - `RED`: `#EF4444` (rojo)
  - `GREEN`: `#22C55E` (verde)
  - `YELLOW`: `#EAB308` (amarillo)
  - `FAULT`: `#6B7280` (gris) + parpadeo
- Cuando `FAULT`, animar con opacity pulsante (CSS animation)
- Mostrar ID del semáforo pequeño debajo
- Tooltip con estado completo al hover

**Implementación sugerida:**
```jsx
export function TrafficLight({ id, state, position }) {
  const colorMap = {
    RED: "#EF4444",
    GREEN: "#22C55E",
    YELLOW: "#EAB308",
    FAULT: "#6B7280"
  };

  return (
    <div
      className="absolute flex flex-col items-center"
      style={{ left: position.x * 80, top: position.y * 80 }}
    >
      <div
        className={`w-12 h-12 rounded-full shadow-lg transition-colors duration-300 ${
          state === "FAULT" ? "animate-pulse" : ""
        }`}
        style={{ backgroundColor: colorMap[state] }}
        title={`${id}: ${state}`}
      />
      <span className="text-xs text-gray-400 mt-1">{id}</span>
    </div>
  );
}
```

**Notas:**
- `position` es en unidades de celda (multiplicar por tamaño de celda)
- Usar `absolute` para posicionar sobre el grid
- Animación de pulsación para FAULT: `animate-pulse` de Tailwind

---

## Tarea 18: `frontend/src/components/VehicleMarker.jsx` — Marcador de Vehículo

**Archivo a crear:** `frontend/src/components/VehicleMarker.jsx`

**Descripción:**
Componente que representa un vehículo en movimiento sobre el grid.

**Props:**
```javascript
{
  id: string,
  status: "WAITING" | "MOVING" | "DONE" | "BLOCKED",
  priority: "EMERGENCY" | "HIGH" | "NORMAL",
  currentPosition: { x: number, y: number },  // coordenadas en el grid
  route: string[]  // ids de intersecciones en la ruta
}
```

**Requisitos visuales:**
- Icono o forma que represente el vehículo:
  - `EMERGENCY`: 🚑 (ambulancia) - color rojo
  - `HIGH`: 🚌 (bus) - color amarillo
  - `NORMAL`: 🚗 (auto) - color azul/gris
- Tamaño pequeño (~20-24px)
- Posición absoluta sobre el grid
- Transición suave cuando cambia de posición (`transition-all duration-300`)
- Mostrar cuando status es `MOVING`, oculto o semitransparente cuando `WAITING`

**Implementación sugerida:**
```jsx
const priorityIcons = {
  EMERGENCY: "🚑",
  HIGH: "🚌",
  NORMAL: "🚗"
};

export function VehicleMarker({ id, status, priority, currentPosition, route }) {
  if (status === "DONE") return null;

  return (
    <div
      className={`absolute text-xl transition-all duration-300 ${
        status === "WAITING" ? "opacity-30" : "opacity-100"
      } ${status === "BLOCKED" ? "grayscale" : ""}`}
      style={{
        left: currentPosition.x * 80 + 20,
        top: currentPosition.y * 80 + 20
      }}
      title={`${id} (${priority}) - ${status}`}
    >
      {priorityIcons[priority]}
    </div>
  );
}
```

**Notas:**
- `currentPosition` viene como `{x, y}` desde el backend (derivado del intersection_id)
- `currentPosition` puede ser la coordenada de la intersección actual o intermedia entre dos intersecciones
- Usar emoji para simplicidad

---

## Tarea 19: `frontend/src/components/IntersectionGrid.jsx` — Grid de Intersecciones

**Archivo a crear:** `frontend/src/components/IntersectionGrid.jsx`

**Descripción:**
Componente principal que renderiza la grilla N×M de intersecciones con semáforos y vehículos.

**Props (desde useWebSocket):**
```javascript
{
  intersections: [{
    id: string,
    state: "RED" | "GREEN" | "YELLOW" | "FAULT",
    position: { x: number, y: number }
  }],
  vehicles: [{
    id: string,
    status: string,
    priority: string,
    currentPosition: { x: number, y: number },
    route: string[]
  }]
}
```

**Requisitos visuales:**
- Grid CSS con columnas y filas que se ajuste al número de intersecciones
- Cada celda representa una intersección
- Líneas de conexión entre celdas adyacentes (calles)
- Renderizar `TrafficLight` en cada celda
- Renderizar `VehicleMarker` sobre las celdas según posición
- Fondo oscuro tipo ciudad noche

**Estructura del grid:**
```jsx
import { TrafficLight } from "./TrafficLight";
import { VehicleMarker } from "./VehicleMarker";

const CELL_SIZE = 80;

export function IntersectionGrid({ intersections, vehicles }) {
  const cols = 3; // grid 3x3

  const gridStyle = {
    display: "grid",
    gridTemplateColumns: `repeat(${cols}, ${CELL_SIZE}px)`,
    gridTemplateRows: `repeat(${cols}, ${CELL_SIZE}px)`,
    gap: "4px"
  };

  return (
    <div className="relative bg-gray-900 p-4 rounded-xl">
      {/* Capa de vehículos (sobre las intersecciones) */}
      <div className="absolute inset-0 pointer-events-none" style={{ zIndex: 10 }}>
        {vehicles.map(v => (
          <VehicleMarker
            key={v.id}
            id={v.id}
            status={v.status}
            priority={v.priority}
            currentPosition={v.currentPosition}
            route={v.route}
          />
        ))}
      </div>

      {/* Grid de semáforos */}
      <div style={gridStyle}>
        {intersections.map(intersection => (
          <TrafficLight
            key={intersection.id}
            id={intersection.id}
            state={intersection.state}
            position={intersection.position}
          />
        ))}
      </div>
    </div>
  );
}
```

**Notas:**
- `currentPosition` del vehículo ya viene como `{x, y}` desde el backend
- La capa de vehículos usa `pointer-events-none` para no interferir con clics
- El grid asume una cuadrícula de 3×3 (configurable)

---

## Tarea 20: `frontend/src/components/ControlPanel.jsx` — Panel de Control Admin

**Archivo a crear:** `frontend/src/components/ControlPanel.jsx`

**Descripción:**
Panel de administración para usuarios con rol `control`. Permite modificar tiempos de semáforos, simular fallos, y controlar la simulación.

**Requisitos UI:**
- Solo visible para usuarios con rol `control`
- Sección de control de simulación: Start/Stop
- Sección de configuración de semáforos: sliders para green_time y red_time
- Botón "Simular Fallo" por intersección
- Botón "Agregar Emergencia" para testing
- Indicador de estado de simulación (running/stopped)

**Estructura del componente:**
```jsx
import { useState } from "react";
import { api } from "../services/api";

export function ControlPanel({ intersections, simulationRunning, onSimulationChange }) {
  const [selectedIntersection, setSelectedIntersection] = useState(null);
  const [greenTime, setGreenTime] = useState(10);
  const [redTime, setRedTime] = useState(10);
  const [loading, setLoading] = useState(false);

  const handleStartStop = async () => {
    setLoading(true);
    try {
      if (simulationRunning) {
        await api.stopSimulation();
      } else {
        await api.startSimulation();
      }
      onSimulationChange?.(!simulationRunning);
    } catch (err) {
      console.error("Simulation control error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateTiming = async () => {
    if (!selectedIntersection) return;
    setLoading(true);
    try {
      await api.updateLightTiming(selectedIntersection, greenTime, redTime);
    } catch (err) {
      console.error("Update timing error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleTriggerFault = async (id) => {
    try {
      await api.triggerFault(id);
    } catch (err) {
      console.error("Trigger fault error:", err);
    }
  };

  const handleAddVehicle = async (priority) => {
    try {
      const route = intersections.slice(0, 3).map(i => i.id);
      const prefix = priority === "EMERGENCY" ? "emergency" : priority === "HIGH" ? "bus" : "car";
      await api.addVehicle(`${prefix}-${Date.now()}`, route, priority);
    } catch (err) {
      console.error("Add vehicle error:", err);
    }
  };

  return (
    <div className="bg-gray-800 p-6 rounded-lg text-white w-80">
      <h2 className="text-xl font-bold mb-4">Panel de Control</h2>

      {/* Simulation Control */}
      <div className="mb-6 p-4 bg-gray-700 rounded">
        <h3 className="font-semibold mb-3">Simulación</h3>
        <div className="flex gap-2 flex-wrap">
          <button
            onClick={handleStartStop}
            disabled={loading}
            className={`px-4 py-2 rounded font-medium ${
              simulationRunning
                ? "bg-red-600 hover:bg-red-700"
                : "bg-green-600 hover:bg-green-700"
            }`}
          >
            {loading ? "..." : simulationRunning ? "Detener" : "Iniciar"}
          </button>
          <button
            onClick={() => handleAddVehicle("EMERGENCY")}
            className="px-4 py-2 bg-red-600 hover:bg-red-700 rounded font-medium"
          >
            🚑 Emergencia
          </button>
          <button
            onClick={() => handleAddVehicle("NORMAL")}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded font-medium"
          >
            🚗 Vehículo
          </button>
        </div>
      </div>

      {/* Traffic Light Configuration */}
      <div className="mb-6 p-4 bg-gray-700 rounded">
        <h3 className="font-semibold mb-3">Configurar Semáforo</h3>

        <select
          value={selectedIntersection || ""}
          onChange={(e) => setSelectedIntersection(e.target.value)}
          className="w-full bg-gray-600 p-2 rounded mb-3 text-white"
        >
          <option value="">Seleccionar intersección...</option>
          {intersections.map(i => (
            <option key={i.id} value={i.id}>{i.id}</option>
          ))}
        </select>

        <div className="space-y-3">
          <div>
            <label className="block text-sm text-gray-300">Verde: {greenTime}s</label>
            <input
              type="range"
              min="3"
              max="30"
              value={greenTime}
              onChange={(e) => setGreenTime(Number(e.target.value))}
              className="w-full"
            />
          </div>
          <div>
            <label className="block text-sm text-gray-300">Rojo: {redTime}s</label>
            <input
              type="range"
              min="3"
              max="30"
              value={redTime}
              onChange={(e) => setRedTime(Number(e.target.value))}
              className="w-full"
            />
          </div>
          <button
            onClick={handleUpdateTiming}
            disabled={!selectedIntersection || loading}
            className="w-full bg-blue-600 hover:bg-blue-700 p-2 rounded disabled:opacity-50"
          >
            Actualizar Tiempos
          </button>
        </div>
      </div>

      {/* Manual Fault Trigger */}
      <div className="p-4 bg-gray-700 rounded">
        <h3 className="font-semibold mb-3">Simular Fallo</h3>
        <div className="grid grid-cols-2 gap-2 max-h-40 overflow-y-auto">
          {intersections.map(i => (
            <button
              key={i.id}
              onClick={() => handleTriggerFault(i.id)}
              className="px-3 py-1 bg-red-600/50 hover:bg-red-600 rounded text-sm"
            >
              {i.id}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
```

**Notas:**
- Recibe `simulationRunning` y `onSimulationChange` como props (el estado lo maneja App.jsx)
- Las props `intersections` vienen del estado de `useWebSocket`
- Verificar `user_role` desde localStorage para mostrar/ocultar el panel en App.jsx
- Usar sliders HTML nativos (`<input type="range">`)

---

## Tarea 21: `frontend/src/App.jsx` — Integración Completa

**Archivo a modificar:** `frontend/src/App.jsx`

**Descripción:**
Componente principal que integra LoginForm, IntersectionGrid, ControlPanel, AlertBanner, y toda la lógica de conexión WebSocket.

**Requisitos:**
1. Pantalla de Login cuando no hay token
2. Dashboard principal con grid y control cuando está autenticado
3. Navbar con indicador de conexión WebSocket, rol y logout
4. Responsive layout (grid + panel lateral en desktop, apilado en mobile)
5. Sincronizar estado de simulación al cargar

**Estructura propuesta:**
```jsx
import { useState, useEffect } from "react";
import { LoginForm } from "./components/LoginForm";
import { IntersectionGrid } from "./components/IntersectionGrid";
import { ControlPanel } from "./components/ControlPanel";
import { AlertBanner } from "./components/AlertBanner";
import { useWebSocket } from "./hooks/useWebSocket";
import { api } from "./services/api";

function App() {
  const [userRole, setUserRole] = useState(null);
  const [simulationRunning, setSimulationRunning] = useState(false);

  // Restaurar sesión al recargar
  useEffect(() => {
    const savedToken = localStorage.getItem("token");
    const savedRole = localStorage.getItem("user_role");
    if (savedToken && savedRole) {
      api.setToken(savedToken);
      setUserRole(savedRole);
    }
  }, []);

  // Sincronizar estado de simulación al autenticarse
  useEffect(() => {
    if (userRole) {
      api.getStatus()
        .then(status => setSimulationRunning(status.running))
        .catch(() => {});
    }
  }, [userRole]);

  // WebSocket state
  const wsState = useWebSocket();

  const handleLogin = (role) => {
    setUserRole(role);
  };

  const handleLogout = () => {
    api.setToken(null);
    localStorage.removeItem("token");
    localStorage.removeItem("user_role");
    setUserRole(null);
    setSimulationRunning(false);
  };

  // Pantalla de login
  if (!userRole) {
    return <LoginForm onLogin={handleLogin} />;
  }

  // Dashboard principal
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <AlertBanner alerts={wsState.alerts} />

      {/* Navbar */}
      <nav className="bg-gray-800 p-4 flex items-center justify-between">
        <h1 className="text-xl font-bold">🚦 Traffic Control System</h1>
        <div className="flex items-center gap-4">
          <span className={wsState.connected ? "text-green-400" : "text-red-400"}>
            {wsState.connected ? "🟢 Conectado" : "🔴 Desconectado"}
          </span>
          <span className="text-sm text-gray-300">
            Rol: <span className="font-semibold">{userRole}</span>
          </span>
          <button
            onClick={handleLogout}
            className="px-3 py-1 bg-red-600 hover:bg-red-700 rounded text-sm"
          >
            Logout
          </button>
        </div>
      </nav>

      {/* Contenido principal */}
      <div className="container mx-auto p-6">
        <div className="flex flex-col lg:flex-row gap-6">
          {/* Grid de intersecciones */}
          <div className="flex-1">
            <IntersectionGrid
              intersections={wsState.intersections}
              vehicles={wsState.vehicles}
            />
          </div>

          {/* Panel de control (solo rol control) */}
          {userRole === "control" && (
            <ControlPanel
              intersections={wsState.intersections}
              simulationRunning={simulationRunning}
              onSimulationChange={setSimulationRunning}
            />
          )}
        </div>

        {/* Stats bar */}
        <div className="mt-6 flex gap-6 text-gray-400 text-sm">
          <span>🚗 Vehículos: {wsState.vehicles.length}</span>
          <span>🚦 Intersecciones: {wsState.intersections.length}</span>
          <span>⚠️ Alertas activas: {wsState.alerts.length}</span>
        </div>
      </div>
    </div>
  );
}

export default App;
```

**Notas:**
- `useWebSocket` hook maneja toda la conexión WebSocket y actualiza el estado
- `ControlPanel` solo se muestra si `userRole === "control"`
- El estado `simulationRunning` se sincroniza al cargar y al iniciar/detener
- Layout responsive: sidebar en desktop, apilado en mobile

---

## Tarea 22: Integrar FaultHandler en la Simulación

**Archivos a modificar:**
- `backend/api/routes_simulation.py`

**Descripción:**
Conectar `FaultHandler` (ya implementado en `core/fault_handler.py`) al flujo de `start_simulation()` para que los fallos aleatorios en semáforos ocurran automáticamente y se reflejen en el frontend.

**Cambios necesarios:**

1. Agregar imports en `routes_simulation.py`:
```python
from core.fault_handler import FaultHandler
from db.database import get_db
from db.models import EventLog
from datetime import datetime
```

2. Agregar variable global:
```python
_fault_handler: FaultHandler | None = None
```

3. En `start_simulation()`, después de crear el engine, instanciar y arrancar FaultHandler:
```python
from db.database import SessionLocal

# Crear fault handler con callbacks de broadcast
async def broadcast_event(event_data: dict):
    await manager.broadcast(event_data)

def on_fault(intersection_id: str):
    """Callback cuando ocurre un fallo."""
    timestamp = datetime.utcnow().isoformat()
    # Broadcast por WebSocket
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(broadcast_event({
        "type": "FAULT",
        "intersection_id": intersection_id,
        "timestamp": timestamp
    }))
    loop.close()
    # Log en DB
    db = SessionLocal()
    try:
        log = EventLog(
            timestamp=timestamp,
            event_type="FAULT",
            intersection_id=intersection_id,
            details='{"source": "fault_handler"}'
        )
        db.add(log)
        db.commit()
    finally:
        db.close()

def on_restore(intersection_id: str):
    """Callback cuando se recupera un fallo."""
    timestamp = datetime.utcnow().isoformat()
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(broadcast_event({
        "type": "RESTORE",
        "intersection_id": intersection_id,
        "timestamp": timestamp
    }))
    loop.close()

_fault_handler = FaultHandler(_network, on_fault, on_restore)
_fault_handler.start()
```

4. En `stop_simulation()`, detener FaultHandler:
```python
global _engine, _fault_handler

if _fault_handler:
    _fault_handler.stop()
    _fault_handler = None
```

**Formato de mensajes WebSocket que debe emitir:**
```json
// Cuando ocurre un fallo:
{"type": "FAULT", "intersection_id": "intersection_0_1", "timestamp": "2026-05-21T12:00:00"}

// Cuando se recupera:
{"type": "RESTORE", "intersection_id": "intersection_0_1", "timestamp": "2026-05-21T12:00:05"}
```

**Notas:**
- `FaultHandler` ya implementa el loop de fallos aleatorios (cada 15-30s) y auto-recuperación (5s)
- Los callbacks `on_fault` y `on_restore` deben crear su propio event loop porque se ejecutan desde un thread secundario
- Los eventos deben loguearse en `EventLog` para persistencia y consulta via `GET /control/logs`
- El frontend `useWebSocket.js` ya maneja mensajes de tipo `FAULT` y los agrega a `alerts`

---

## Tarea 23: Integrar DeadlockDetector en la Simulación

**Archivos a modificar:**
- `backend/core/scheduler.py`
- `backend/api/routes_simulation.py`

**Descripción:**
Conectar `DeadlockDetector` (ya implementado en `core/deadlock_detector.py`) al flujo de simulación para detectar y resolver vehículos bloqueados por más de 10 segundos.

### Subtarea 23A: Agregar `remove_vehicle()` a TrafficScheduler

En `backend/core/scheduler.py`, agregar método para remover un vehículo de todas las colas:

```python
def remove_vehicle(self, vehicle_id: str):
    """
    Remueve un vehículo de todas las colas de recursos.
    Se usa cuando un deadlock es detectado (rollback).
    """
    with self._lock:
        # Limpiar event de dispatch
        self._dispatch_events.pop(vehicle_id, None)
        # Nota: PriorityQueue no soporta remoción directa.
        # Reconstruimos cada cola filtrando el vehículo.
        for inter_id in list(self._queues.keys()):
            q = self._queues[inter_id]
            remaining = []
            while not q.empty():
                try:
                    item = q.get_nowait()
                    # item = (priority, timestamp, vehicle)
                    if item[2].vehicle_id != vehicle_id:
                        remaining.append(item)
                except queue.Empty:
                    break
            # Re-encolar los que no fueron removidos
            for item in remaining:
                q.put(item)
```

### Subtarea 23B: Conectar DeadlockDetector en `routes_simulation.py`

1. Agregar imports:
```python
from core.deadlock_detector import DeadlockDetector
```

2. Agregar variable global:
```python
_deadlock_detector: DeadlockDetector | None = None
```

3. En `start_simulation()`, instanciar y conectar:
```python
def on_deadlock(vehicle_id: str, intersection_id: str):
    """Callback cuando se detecta un deadlock."""
    timestamp = datetime.utcnow().isoformat()
    # Remover vehículo del scheduler (rollback)
    _scheduler.remove_vehicle(vehicle_id)
    # Broadcast
    async def send():
        await manager.broadcast({
            "type": "DEADLOCK",
            "vehicle_id": vehicle_id,
            "intersection_id": intersection_id,
            "timestamp": timestamp
        })
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send())
    loop.close()
    # Log en DB
    db = SessionLocal()
    try:
        log = EventLog(
            timestamp=timestamp,
            event_type="DEADLOCK",
            vehicle_id=vehicle_id,
            intersection_id=intersection_id,
            details='{"resolution": "rollback_vehicle_removed"}'
        )
        db.add(log)
        db.commit()
    finally:
        db.close()

_deadlock_detector = DeadlockDetector(_scheduler, on_deadlock)
_deadlock_detector.start()
```

4. En `stop_simulation()`:
```python
global _engine, _fault_handler, _deadlock_detector

if _deadlock_detector:
    _deadlock_detector.stop()
    _deadlock_detector = None
```

### Subtarea 23C: Conectar register/unregister en el engine

Modificar `SimulationEngine.add_vehicle()` y el flujo del scheduler para registrar vehículos en el DeadlockDetector. Dado que el DeadlockDetector se crea fuera del engine, la alternativa más limpia es inyectarlo:

Opcional: Pasar `deadlock_detector` al `SimulationEngine` y que este llame `register_vehicle`/`unregister_vehicle` en los momentos adecuados. Para esta entrega, basta con que el DeadlockDetector monitoree los vehículos que están en cola (vía `register_vehicle` llamado desde un wrapper del scheduler).

**Notas:**
- `PriorityQueue` no permite remover elementos arbitrarios. La reconstrucción de cola es la solución aceptable para este alcance académico.
- El callback `on_deadlock` debe remover el vehículo del scheduler para romper el ciclo de espera (rollback).
- `DeadlockDetector.MAX_WAIT_TIME = 10` segundos.

---

## Tarea 24: Normalizar Datos de Vehículos en API y WebSocket

**Archivos a modificar:**
- `backend/simulation/engine.py`
- `backend/api/routes_simulation.py`

**Descripción:**
Los datos de vehículos en `/simulation/status` y en el broadcast `STATE_UPDATE` del WebSocket tienen valores hardcodeados (`route: []`, `priority: "NORMAL"`, `vehicle_count: 0`). Esta tarea normaliza los datos para que el frontend reciba información real.

### Subtarea 24A: state_snapshot() debe incluir route y priority

En `engine.py`, modificar `state_snapshot()`:

```python
def state_snapshot(self) -> dict:
    intersections_state = []
    for inter in self.network.get_all():
        intersections_state.append({
            "id": inter.id,
            "state": inter.light.state
        })

    vehicles_state = []
    for v_id, v in list(self.active_vehicles.items()):
        # Determinar intersección actual basada en la ruta
        current_inter_id = v.route[v.current_position] if v.current_position < len(v.route) else v.route[-1]
        vehicles_state.append({
            "id": v.vehicle_id,
            "status": v.status,
            "position": v.current_position,
            "route": v.route,
            "priority": v.priority.name,  # "EMERGENCY" | "HIGH" | "NORMAL"
            "current_intersection": current_inter_id
        })

    return {
        "intersections": intersections_state,
        "vehicles": vehicles_state,
        "tick": self._tick_count
    }
```

### Subtarea 24B: get_status() debe transformar posición a coordenadas y contar vehículos

En `routes_simulation.py`, modificar `get_status()`:

```python
def _intersection_coords(inter_id: str) -> dict:
    """Deriva coordenadas {x, y} del id de intersección (formato: intersection_i_j)."""
    parts = inter_id.split("_")
    return {"x": int(parts[1]), "y": int(parts[2])}

# En get_status, después de snapshot:
snapshot = _engine.state_snapshot()

# Contar vehículos por intersección
vehicle_counts = {}
for v in snapshot.get("vehicles", []):
    inter_id = v.get("current_intersection", "")
    if inter_id:
        vehicle_counts[inter_id] = vehicle_counts.get(inter_id, 0) + 1

return {
    "running": _engine._tick_thread is not None and _engine._tick_thread.is_alive(),
    "tick": snapshot.get("tick", 0),
    "intersections": [
        {
            "id": inter["id"],
            "state": inter["state"],
            "position": _intersection_coords(inter["id"]),
            "vehicle_count": vehicle_counts.get(inter["id"], 0)
        }
        for inter in snapshot.get("intersections", [])
    ],
    "vehicles": [
        {
            "id": v["id"],
            "status": v["status"],
            "position": v["position"],
            "route": v.get("route", []),
            "priority": v.get("priority", "NORMAL"),
            "currentPosition": _intersection_coords(v.get("current_intersection", "intersection_0_0"))
        }
        for v in snapshot.get("vehicles", [])
    ]
}
```

### Subtarea 24C: Broadcast STATE_UPDATE con datos completos

En `engine.py` `_loop()`, modificar el STATE_UPDATE para incluir la nueva estructura:

```python
if self._broadcast_func:
    snapshot = self.state_snapshot()
    state = {
        "type": "STATE_UPDATE",
        "intersections": snapshot.get("intersections", []),
        "vehicles": snapshot.get("vehicles", []),
        "alerts": [],
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    # broadcast...
```

**Notas:**
- `currentPosition` en el broadcast se calcula derivando las coordenadas {x, y} del `current_intersection`
- El frontend `VehicleMarker` recibe `currentPosition: {x, y}` directamente
- `route` y `priority` reales permiten al frontend mostrar información correcta

---

## Tarea 25: Agregar Soporte de `red_time` en Semáforos

**Archivos a modificar:**
- `backend/core/traffic_light.py`
- `backend/simulation/engine.py`
- `backend/api/routes_control.py`

**Descripción:**
Actualmente el semáforo solo tiene `green_time` y el engine usa `green_time` para ambas fases. El modelo `LightConfig` en DB ya almacena `red_time`, pero no se aplica en runtime.

### Subtarea 25A: Agregar `red_time` a TrafficLight

En `traffic_light.py`:

```python
class TrafficLight:
    def __init__(self, intersection_id: str, green_time: int = 10, red_time: int = 10):
        self.id = intersection_id
        self.state = "RED"
        self.green_time = green_time
        self.red_time = red_time  # Nuevo: tiempo en rojo (independiente del verde)
        # ... resto igual
```

### Subtarea 25B: Usar `red_time` en el engine

En `engine.py` `_loop()`, reemplazar la línea que copia green_time como red_time:

```python
# Antes (línea 80):
current_red_time = light.green_time

# Después:
current_red_time = light.red_time
```

### Subtarea 25C: Aplicar `red_time` desde routes_control

En `routes_control.py`, en `update_timing()`, agregar la asignación de `red_time`:

```python
# Después de actualizar green_time:
intersection.light.green_time = green_time
intersection.light.red_time = red_time  # Nueva línea
```

**Notas:**
- El frontend `ControlPanel` ya envía `red_time` en el body de `PUT /control/lights/{id}/timing`
- La DB ya persiste `red_time` en la tabla `light_config`
- Esta tarea completa el ciclo: ControlPanel → API → TrafficLight → Engine

---

## Tarea 26: Variables de Entorno — Frontend

**Archivo a crear/modificar:** `frontend/.env`

**Descripción:**
Archivo de variables de entorno para desarrollo local.

```
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws
```

**Notas:**
- Las variables `VITE_` son expuestas por Vite al frontend
- `VITE_API_URL` es usada por `services/api.js`
- `VITE_WS_URL` es usada por `hooks/useWebSocket.js`

---

## Tarea 27: Integración y Pruebas

**Descripción:**
Verificar que todo funcione correctamente end-to-end.

### Pasos de verificación

```bash
# Terminal 1 - Backend
cd backend && source .venv/bin/activate && rm -f traffic.db && uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend && npm run dev

# Terminal 3 - Pruebas API
```

**Pruebas manuales:**

1. **Registro y Login:**
   ```bash
   curl -X POST http://localhost:8000/auth/register \
     -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"admin123","role":"control"}'
   
   curl -X POST http://localhost:8000/auth/login \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=admin123"
   ```

2. **Iniciar simulación:**
   ```bash
   TOKEN="<token_del_login>"
   curl -X POST http://localhost:8000/simulation/start \
     -H "Authorization: Bearer $TOKEN"
   ```

3. **Verificar estado con datos completos:**
   ```bash
   curl http://localhost:8000/simulation/status \
     -H "Authorization: Bearer $TOKEN" | python -m json.tool
   ```
   Verificar que `vehicles` incluya `route`, `priority` y `currentPosition` reales.

4. **Verificar fallos automáticos:** Esperar 15-30s y observar que AlertBanner muestra fallos en el frontend. Verificar log:
   ```bash
   curl http://localhost:8000/control/logs?event_type=FAULT \
     -H "Authorization: Bearer $TOKEN"
   ```

5. **Modificar tiempos desde ControlPanel:**
   ```bash
   curl -X PUT http://localhost:8000/control/lights/intersection_0_0/timing \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"green_time": 5, "red_time": 8}'
   ```
   Verificar que el semáforo cambia de fase según los nuevos tiempos.

6. **Agregar vehículo y ver movimiento:**
   ```bash
   curl -X POST http://localhost:8000/simulation/vehicle \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"id":"test-1","route":["intersection_0_0","intersection_1_0","intersection_2_0"],"priority":"NORMAL"}'
   ```
   Verificar que aparece en el grid y avanza.

7. **Verificar rol viewer:**
   ```bash
   curl -X POST http://localhost:8000/auth/register \
     -H "Content-Type: application/json" \
     -d '{"username":"visor","password":"visor123","role":"viewer"}'
   
   VIEWER_TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=visor&password=visor123" | python -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
   
   # Viewer debe recibir 403 en rutas control
   curl -X POST http://localhost:8000/simulation/start \
     -H "Authorization: Bearer $VIEWER_TOKEN"
   ```

8. **Prueba frontend:** Abrir `http://localhost:5173`, loguearse, iniciar simulación, observar el grid, verificar que AlertBanner muestra fallos.

### Criterios de Aceptación

| # | Criterio | Verificación |
|---|----------|-------------|
| 1 | Login funciona y guarda token | LoginForm + localStorage |
| 2 | Grid muestra intersecciones con colores correctos | Según estado RED/GREEN/YELLOW/FAULT |
| 3 | Vehículos aparecen con prioridad y ruta correctas | `currentPosition` como {x,y} en el grid |
| 4 | ControlPanel visible solo para rol `control` | Viewer no ve el panel |
| 5 | Fallos automáticos aparecen como AlertBanner rojo | FaultHandler emite `type: "FAULT"` por WS |
| 6 | Fallos se recuperan solos a los 5s | AlertBanner + RESTORE event |
| 7 | Cambios en ControlPanel afectan la simulación | Sliders de green_time y red_time funcionales |
| 8 | Vehículo de emergencia (🚑) tiene prioridad sobre normales | Priority Scheduling en acción |
| 9 | DeadlockDetector remueve vehículos bloqueados >10s | Log DEADLOCK en control/logs |
| 10 | WebSocket actualiza UI en tiempo real | STATE_UPDATE cada tick |

---

## Resumen de Entrega 2

### Archivos a crear (nuevos):
1. `frontend/src/components/TrafficLight.jsx`
2. `frontend/src/components/VehicleMarker.jsx`
3. `frontend/src/components/IntersectionGrid.jsx`
4. `frontend/src/components/ControlPanel.jsx`
5. `frontend/.env`

### Archivos a modificar:
6. `frontend/src/App.jsx` — Integración completa con ControlPanel y datos reales
7. `backend/api/routes_simulation.py` — Conectar FaultHandler + DeadlockDetector + datos normalizados
8. `backend/simulation/engine.py` — state_snapshot() con route, priority, current_intersection
9. `backend/core/traffic_light.py` — Agregar red_time attribute
10. `backend/core/scheduler.py` — Agregar remove_vehicle() para rollback de deadlock
11. `backend/api/routes_control.py` — Aplicar red_time al TrafficLight

### Resumen de componentes del sistema

```
Frontend (React + Vite + Tailwind)
├── App.jsx                    → Layout, login, dashboard, routing
├── components/
│   ├── LoginForm.jsx          → Login con JWT
│   ├── AlertBanner.jsx        → Alertas FAULT/EMERGENCY/DEADLOCK
│   ├── TrafficLight.jsx       → Semáforo visual con colores y animación
│   ├── VehicleMarker.jsx      → Vehículo animado en grid
│   ├── IntersectionGrid.jsx   → Grid 3×3 con semáforos + vehículos
│   └── ControlPanel.jsx       → Start/Stop, sliders, fallos manuales
├── hooks/
│   └── useWebSocket.js        → WS connection + auto-reconnect
└── services/
    └── api.js                 → REST client con JWT

Backend (FastAPI + SQLite + threading)
├── main.py                    → Entry point, routers, CORS
├── config.py                  → Settings globales (Pydantic)
├── auth/
│   ├── jwt_handler.py         → create_token, decode_token, get_current_user
│   └── roles.py               → require_role, require_any_role, get_optional_user
├── api/
│   ├── routes_auth.py         → POST /auth/register, POST /auth/login
│   ├── routes_simulation.py   → Inicia/stop, estado, vehiculos + FaultHandler+DeadlockDetector
│   ├── routes_control.py      → Timing, fallos manuales, logs → aplica red_time
│   └── websocket.py           → ConnectionManager + /ws endpoint
├── db/
│   ├── database.py            → SQLAlchemy engine + get_db
│   └── models.py              → User, EventLog, LightConfig
├── core/
│   ├── traffic_light.py       → Semáforo con red_time, green_time, fault_event
│   ├── vehicle.py             → Vehicle(Thread) con prioridad y ruta
│   ├── scheduler.py           → Priority Scheduling + remove_vehicle()
│   ├── intersection.py        → Nodo con TrafficLight
│   ├── fault_handler.py       → Fallos aleatorios + auto-recuperación
│   └── deadlock_detector.py   → Timeout ≥10s → rollback
└── simulation/
    ├── engine.py              → Kernel loop, active_vehicles, state_snapshot()
    └── network.py             → Grafo de intersecciones (Resource Allocation Graph)
```

### Criterios de Aceptación Final:
- [ ] Sistema completo start-to-end funcionando
- [ ] Todos los conceptos de SO mapeados correctamente en código
- [ ] WebSocket actualiza UI en tiempo real con STATE_UPDATE
- [ ] FaultHandler dispara fallos aleatorios cada 15-30s con broadcast FAULT
- [ ] Auto-recuperación de fallos a los 5s con broadcast RESTORE
- [ ] DeadlockDetector remueve vehículos bloqueados >10s con broadcast DEADLOCK
- [ ] Vehículos muestran ruta, prioridad y posición correcta en el grid
- [ ] Los tiempos red_time y green_time se aplican realmente al ciclo del semáforo
- [ ] Auth JWT protege rutas sensibles
- [ ] Roles viewer/control aplicados correctamente en frontend y backend
- [ ] AlertBanner muestra fallos, emergencias y deadlocks en tiempo real
- [ ] Panel de control permite modificar tiempos (verde y rojo) de semáforos

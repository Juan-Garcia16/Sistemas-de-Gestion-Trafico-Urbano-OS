# ENTREGA 2: Frontend Completo + Integración Final

## Objetivo de la Entrega
Frontend visual completo con grid de intersecciones, semáforos animados, vehículos en movimiento, panel de control y login. Sistema integrado funcionando end-to-end.

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
- El color puede ser clase Tailwind o style inline
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
  currentPosition: { x: number, y: number },  // posición en el grid
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
- Mostrar cuando status es `MOVING`, invisible o diferente cuando `WAITING`

**Estilos por prioridad:**
```css
.emergency { color: #EF4444; }
.high { color: #EAB308; }
.normal { color: #3B82F6; }
```

**Implementación sugerida:**
```jsx
const priorityIcons = {
  EMERGENCY: "🚑",
  HIGH: "🚌",
  NORMAL: "🚗"
};

export function VehicleMarker({ id, status, priority, currentPosition, route }) {
  if (status === "WAITING" || status === "DONE") {
    return null; // No mostrar cuando está esperando o llegó
  }

  return (
    <div
      className={`absolute text-xl transition-all duration-300 ${
        status === "BLOCKED" ? "opacity-50" : "opacity-100"
      }`}
      style={{
        left: currentPosition.x * 80 + 20, // offset para centrar en celda
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
- Calcular `currentPosition` basado en `route[position]` o directamente de los datos del engine
- Usar emoji para simplicidad, o SVG para mejor calidad visual
- La posición debe interpolarse suavemente con CSS transitions

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
    position: number,  // índice en la ruta actual
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
const GRID_COLS = 4;  // configurable
const CELL_SIZE = 80; // pixels

export function IntersectionGrid({ intersections, vehicles }) {
  // Crear mapa de intersecciones para acceso rápido
  const intersectionMap = Object.fromEntries(
    intersections.map(i => [i.id, i])
  );

  // Posición del grid (responsive)
  const gridStyle = {
    display: "grid",
    gridTemplateColumns: `repeat(${GRID_COLS}, ${CELL_SIZE}px)`,
    gap: "4px"
  };

  return (
    <div className="relative bg-gray-900 p-4 rounded-xl">
      {/* Líneas de calles como background */}
      <div className="absolute inset-4 grid-lines" />

      {/* Contenedor de vehículos (layer superior) */}
      <div className="absolute inset-0 pointer-events-none">
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
- La posición de cada vehículo debe calcularse basado en su ruta actual
- Si `currentPosition` es índice en `route`, entonces la posición del vehículo es `route[currentPosition]`
- Usar `absolute` positioning para los vehículos sobre el grid
- El grid puede tener líneas de "calles" usando pseudo-elements o divs adicionales

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

export function ControlPanel({ intersections, onSimulationChange }) {
  const [selectedIntersection, setSelectedIntersection] = useState(null);
  const [greenTime, setGreenTime] = useState(10);
  const [redTime, setRedTime] = useState(10);
  const [loading, setLoading] = useState(false);
  const [simulationRunning, setSimulationRunning] = useState(false);

  const handleStartStop = async () => {
    setLoading(true);
    try {
      if (simulationRunning) {
        await api.stopSimulation();
      } else {
        await api.startSimulation();
      }
      setSimulationRunning(!simulationRunning);
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

  const handleAddEmergency = async () => {
    try {
      const route = intersections.slice(0, 3).map(i => i.id);
      await api.addVehicle(`emergency-${Date.now()}`, route, "EMERGENCY");
    } catch (err) {
      console.error("Add emergency error:", err);
    }
  };

  return (
    <div className="bg-gray-800 p-6 rounded-lg text-white">
      <h2 className="text-xl font-bold mb-4">Panel de Control</h2>

      {/* Simulation Control */}
      <div className="mb-6 p-4 bg-gray-700 rounded">
        <h3 className="font-semibold mb-3">Simulación</h3>
        <div className="flex gap-3">
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
            onClick={handleAddEmergency}
            className="px-4 py-2 bg-yellow-600 hover:bg-yellow-700 rounded font-medium"
          >
            + Emergencia
          </button>
        </div>
      </div>

      {/* Traffic Light Configuration */}
      <div className="mb-6 p-4 bg-gray-700 rounded">
        <h3 className="font-semibold mb-3">Configurar Semáforo</h3>

        <select
          value={selectedIntersection || ""}
          onChange={(e) => setSelectedIntersection(e.target.value)}
          className="w-full bg-gray-600 p-2 rounded mb-3"
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
        <div className="grid grid-cols-2 gap-2">
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
- El componente recibe `intersections` y `onSimulationChange` como props
- `intersections` viene del estado de `useWebSocket`
- Verificar `user_role` desde localStorage para mostrar/ocultar el panel
- Usar API real de Tailwind para sliders (`<input type="range">`)

---

## Tarea 21: `frontend/src/App.jsx` — Integración Completa

**Archivo a crear:** `frontend/src/App.jsx`

**Descripción:**
Componente principal que integra LoginForm, IntersectionGrid, ControlPanel, AlertBanner, y toda la lógica de conexión WebSocket.

**Requisitos:**
1. Pantalla de Login cuando no hay token
2. Dashboard principal con grid y control cuando está autenticado
3. Sidemenu o navbar con logout
4. Responsive layout

**Estructura propuesta:**
```jsx
import { useState, useEffect } from "react";
import { LoginForm } from "./components/LoginForm";
import { IntersectionGrid } from "./components/IntersectionGrid";
import { TrafficLight } from "./components/TrafficLight";
import { VehicleMarker } from "./components/VehicleMarker";
import { ControlPanel } from "./components/ControlPanel";
import { AlertBanner } from "./components/AlertBanner";
import { useWebSocket } from "./hooks/useWebSocket";
import { api } from "./services/api";

function App() {
  const [userRole, setUserRole] = useState(null);
  const [showControlPanel, setShowControlPanel] = useState(true);

  // Verificar si hay sesión guardada
  useEffect(() => {
    const savedToken = localStorage.getItem("token");
    const savedRole = localStorage.getItem("user_role");
    if (savedToken && savedRole) {
      api.setToken(savedToken);
      setUserRole(savedRole);
    }
  }, []);

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
  };

  // Login screen
  if (!userRole) {
    return <LoginForm onLogin={handleLogin} />;
  }

  // Main dashboard
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Navigation */}
      <nav className="bg-gray-800 p-4 flex justify-between items-center">
        <h1 className="text-xl font-bold">🚦 Traffic Control System</h1>
        <div className="flex items-center gap-4">
          <span className="text-gray-400">
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

      {/* Alerts */}
      <AlertBanner alerts={wsState.alerts} />

      {/* Main content */}
      <div className="container mx-auto p-6">
        <div className="flex gap-6">
          {/* Grid principal */}
          <div className="flex-1">
            <IntersectionGrid
              intersections={wsState.intersections}
              vehicles={wsState.vehicles}
            />
          </div>

          {/* Panel de control (solo rol control) */}
          {userRole === "control" && showControlPanel && (
            <div className="w-80">
              <ControlPanel
                intersections={wsState.intersections}
                onSimulationChange={(running) => {}}
              />
            </div>
          )}
        </div>

        {/* Stats bar */}
        <div className="mt-6 flex gap-6 text-gray-400">
          <span>🚗 Vehículos: {wsState.vehicles.length}</span>
          <span>🚦 Intersecciones: {wsState.intersections.length}</span>
        </div>
      </div>
    </div>
  );
}

export default App;
```

**Notas:**
- `useWebSocket` hook maneja toda la conexión WebSocket
- El componente es "dummy receiver" - solo recibe props de los hooks
- ControlPanel solo se muestra si `userRole === "control"`
- Usar `useEffect` para restaurar sesión en reload

---

## Tarea 22: Archivos faltantes - Imports y Exports

**Archivos a crear:**
- `frontend/src/hooks/__init__.py` (vacío, solo para que sea módulo)
- `frontend/src/services/__init__.py` (vacío)
- `frontend/src/components/__init__.py` (vacío)
- `frontend/src/__init__.py` (vacío)

**Descripción:**
Crear archivos `__init__.py` vacíos en los directorios correspondientes para que Python/Node pueda importar correctamente los módulos.

---

## Tarea 23: Variables de Entorno - Frontend

**Archivo a crear:** `frontend/.env`

**Descripción:**
Archivo de variables de entorno para desarrollo local.

```
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws
```

---

## Tarea 24: Integración y Pruebas

**Descripción:**
Verificar que todo funcione correctamente end-to-end.

**Pasos de verificación:**
1. Backend inicia: `cd backend && uvicorn main:app --reload --port 8000`
2. Frontend inicia: `cd frontend && npm run dev`
3. Registro de usuario via POST /auth/register
4. Login y obtención de JWT
5. Inicio de simulación via POST /simulation/start
6. Verificar que WebSocket recibe STATE_UPDATE
7. Verificar que AlertBanner muestra alertas de fallos
8. Verificar que ControlPanel actualiza tiempos de semáforos
9. Verificar que IntersectionGrid muestra todos los elementos

**Criterios de aceptación:**
- [ ] Login funciona y guarda token
- [ ] Grid muestra intersecciones con colores correctos
- [ ] Vehículos aparecen y se mueven
- [ ] ControlPanel visible solo para rol `control`
- [ ] Fallos se muestran como alertas
- [ ] Cambios en ControlPanel afectan la simulación

---

## Resumen de Entrega 2

### Archivos a crear (Frontend):

| # | Archivo | Descripción |
|---|---------|-------------|
| 17 | `src/components/TrafficLight.jsx` | Semáforo visual con colores |
| 18 | `src/components/VehicleMarker.jsx` | Marcador de vehículo animado |
| 19 | `src/components/IntersectionGrid.jsx` | Grid de intersecciones completo |
| 20 | `src/components/ControlPanel.jsx` | Panel de administración |
| 21 | `src/App.jsx` | Integración completa de toda la UI |
| 22 | `src/hooks/__init__.py` | Módulo Python |
| 22 | `src/services/__init__.py` | Módulo Python |
| 22 | `src/components/__init__.py` | Módulo Python |
| 22 | `src/__init__.py` | Módulo Python |
| 23 | `.env` | Variables de entorno |
| 24 | Pruebas de integración | Verificación manual |

### Criterios de Aceptación Final:
- [ ] Sistema completo start-to-end funcionando
- [ ] Todos los conceptos de SO mapeados correctamente en código
- [ ] WebSocket actualiza UI en tiempo real
- [ ] Auth JWT protege rutas sensibles
- [ ] Roles viewer/control aplicados correctamente
- [ ] FaultHandler dispara fallos aleatorios cada 15-30s
- [ ] Auto-recuperación de fallos a los 5s
- [ ] Fallos visibles como AlertBanner en frontend
- [ ] Panel de control permite modificar tiempos de semáforos
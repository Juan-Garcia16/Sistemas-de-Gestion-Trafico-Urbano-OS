import { useState } from "react";
import { api } from "../services/api";

const TABS = [
  { id: "simulation", label: "▶ Simulación" },
  { id: "demos", label: "🎬 Demos" },
  { id: "config", label: "⚙️ Semáforos" }
];

export function ControlPanel({ intersections, simulationRunning, onSimulationChange }) {
  const [activeTab, setActiveTab] = useState("simulation");
  const [selectedIntersection, setSelectedIntersection] = useState("");
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
    try { await api.triggerFault(id); } catch (e) { console.error(e); }
  };

  const handleAddVehicle = async (priority) => {
    try {
      const route = intersections.slice(0, 3).map(i => i.id);
      const prefix = priority === "EMERGENCY" ? "emergency" : "car";
      await api.addVehicle(`${prefix}-${Date.now()}`, route, priority);
    } catch (err) { console.error(err); }
  };

  const handleScenario = async (scenario) => {
    try { await api.runScenario(scenario); } catch (e) { console.error(e); }
  };

  // Ordenar intersecciones por coordenada y (filas) y luego x (columnas) para corregir el orden de la matriz transpuesta
  const getCoords = (i) => {
    if (i.position) return i.position;
    const parts = i.id.split("_");
    return { x: parseInt(parts[1]) || 0, y: parseInt(parts[2]) || 0 };
  };

  const sortedIntersections = [...intersections].sort((a, b) => {
    const posA = getCoords(a);
    const posB = getCoords(b);
    if (posA.y !== posB.y) {
      return posA.y - posB.y;
    }
    return posA.x - posB.x;
  });

  return (
    <div className="bg-gray-800 rounded-lg text-white w-80 shrink-0 border border-gray-700/60 shadow-xl overflow-hidden overflow-x-hidden">
      {/* Tab header */}
      <div className="flex border-b border-gray-700">
        {TABS.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex-1 p-2.5 text-xs font-semibold transition-colors cursor-pointer ${
              activeTab === tab.id
                ? "bg-gray-700 border-b-2 border-blue-500 text-white text-blue-400 font-bold"
                : "text-gray-400 hover:text-gray-200"
            }`}
          >
            {tab.label.replace(/[▶🎬⚙️]/g, "").trim()}
          </button>
        ))}
      </div>

      {/* Tab content */}
      <div className="p-4 overflow-x-hidden">
        {/* TAB: Simulación */}
        {activeTab === "simulation" && (
          <div className="space-y-3">
            <button
              onClick={handleStartStop}
              disabled={loading}
              className={`w-full px-4 py-2.5 rounded font-bold text-sm cursor-pointer transition duration-150 active:scale-98 ${
                simulationRunning
                  ? "bg-red-600 hover:bg-red-700 text-white"
                  : "bg-green-600 hover:bg-green-700 text-white"
              }`}
            >
              {loading ? "..." : simulationRunning ? "Detener Simulación" : "Iniciar Simulación"}
            </button>
            <div className="flex gap-2">
              <button
                onClick={() => handleAddVehicle("EMERGENCY")}
                className="flex-1 px-3 py-2 bg-red-600 hover:bg-red-700 rounded text-xs font-semibold cursor-pointer transition active:scale-98"
              >
                Emergencia P0
              </button>
              <button
                onClick={() => handleAddVehicle("NORMAL")}
                className="flex-1 px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded text-xs font-semibold cursor-pointer transition active:scale-98"
              >
                Vehículo P2
              </button>
            </div>
          </div>
        )}

        {/* TAB: Demos */}
        {activeTab === "demos" && (
          <div className="space-y-2">
            <button
              onClick={() => handleScenario("mutex_demo")}
              className="w-full px-3 py-2.5 bg-purple-600 hover:bg-purple-700 rounded text-xs font-bold cursor-pointer text-left transition duration-150 active:scale-98"
            >
              🔒 Exclusión Mutua
              <span className="block text-[10px] text-purple-300 font-medium font-mono mt-0.5 break-words">3 vehículos → misma intersección</span>
            </button>
            <button
              onClick={() => handleScenario("priority_demo")}
              className="w-full px-3 py-2.5 bg-yellow-600 hover:bg-yellow-700 rounded text-xs font-bold cursor-pointer text-left transition duration-150 active:scale-98"
            >
              🚑 Planificación por Prioridad
              <span className="block text-[10px] text-yellow-300 font-medium font-mono mt-0.5 break-words">Emergencia P0 gana a normales P2</span>
            </button>
            <button
              onClick={() => handleScenario("deadlock_demo")}
              className="w-full px-3 py-2.5 bg-red-700 hover:bg-red-800 rounded text-xs font-bold cursor-pointer text-left transition duration-150 active:scale-98"
            >
              💀 Deadlock + Rollback
              <span className="block text-[10px] text-red-300 font-medium font-mono mt-0.5 break-words">2 vehículos → interbloqueo → auto-resolución</span>
            </button>
          </div>
        )}

        {/* TAB: Semáforos */}
        {activeTab === "config" && (
          <div className="space-y-3">
            <select
              value={selectedIntersection}
              onChange={(e) => setSelectedIntersection(e.target.value)}
              className="w-full bg-gray-700 border border-gray-600 p-2 rounded text-xs text-white cursor-pointer focus:outline-none focus:ring-1 focus:ring-blue-500"
            >
              <option value="">Seleccionar intersección...</option>
              {intersections.map(i => {
                const parts = i.id.split("_");
                return (
                  <option key={i.id} value={i.id}>
                    Intersección [{parts[1]},{parts[2]}]
                  </option>
                );
              })}
            </select>

            <div>
              <label className="text-[10px] text-gray-400 font-semibold font-mono">🟢 Verde: {greenTime}s</label>
              <input type="range" min="3" max="30" value={greenTime}
                onChange={(e) => setGreenTime(Number(e.target.value))} className="w-full cursor-pointer h-1 bg-gray-700 rounded-lg appearance-none" />
            </div>
            <div>
              <label className="text-[10px] text-gray-400 font-semibold font-mono">🔴 Rojo: {redTime}s</label>
              <input type="range" min="3" max="30" value={redTime}
                onChange={(e) => setRedTime(Number(e.target.value))} className="w-full cursor-pointer h-1 bg-gray-700 rounded-lg appearance-none" />
            </div>
            <button
              onClick={handleUpdateTiming}
              disabled={!selectedIntersection || loading}
              className="w-full bg-blue-600 hover:bg-blue-700 p-2 rounded text-xs font-bold cursor-pointer transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Actualizar Tiempos
            </button>

            <div className="border-t border-gray-700 pt-3">
              <p className="text-[10px] text-gray-400 font-bold uppercase tracking-wider mb-2 font-mono">Inyección de Interrupción (Fallo)</p>
              <div className="grid grid-cols-3 gap-1.5">
                {sortedIntersections.map(i => {
                  const isFaulty = i.state === "FAULT";
                  const parts = i.id.split("_");
                  return (
                    <button
                      key={i.id}
                      onClick={() => handleTriggerFault(i.id)}
                      className={`px-2 py-1.5 rounded text-[10px] font-mono font-bold transition-all duration-200 cursor-pointer ${
                        isFaulty
                          ? "bg-red-600 text-white shadow-lg shadow-red-900/50 animate-pulse border border-red-400"
                          : "bg-red-950/40 hover:bg-red-900/60 text-red-400 hover:text-red-200 border border-red-900/30"
                      }`}
                    >
                      {isFaulty ? "⚠️" : "INT"} {parts[1]},{parts[2]}
                    </button>
                  );
                })}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

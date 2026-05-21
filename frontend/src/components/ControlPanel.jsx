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

  return (
    <div className="bg-gray-800 rounded-lg text-white w-80 shrink-0">
      {/* Tab header */}
      <div className="flex border-b border-gray-700">
        {TABS.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex-1 p-2.5 text-xs font-medium transition-colors ${
              activeTab === tab.id
                ? "bg-gray-700 border-b-2 border-blue-500 text-white"
                : "text-gray-400 hover:text-gray-200"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab content */}
      <div className="p-4">
        {/* TAB: Simulación */}
        {activeTab === "simulation" && (
          <div className="space-y-3">
            <button
              onClick={handleStartStop}
              disabled={loading}
              className={`w-full px-4 py-2.5 rounded font-medium text-sm ${
                simulationRunning
                  ? "bg-red-600 hover:bg-red-700"
                  : "bg-green-600 hover:bg-green-700"
              }`}
            >
              {loading ? "..." : simulationRunning ? "⏹ Detener Simulación" : "▶ Iniciar Simulación"}
            </button>
            <div className="flex gap-2">
              <button
                onClick={() => handleAddVehicle("EMERGENCY")}
                className="flex-1 px-3 py-2 bg-red-600 hover:bg-red-700 rounded text-sm"
              >
                🚑 Emergencia
              </button>
              <button
                onClick={() => handleAddVehicle("NORMAL")}
                className="flex-1 px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded text-sm"
              >
                🚗 Vehículo
              </button>
            </div>
          </div>
        )}

        {/* TAB: Demos */}
        {activeTab === "demos" && (
          <div className="space-y-2">
            <button
              onClick={() => handleScenario("mutex_demo")}
              className="w-full px-3 py-2.5 bg-purple-600 hover:bg-purple-700 rounded text-sm font-medium"
            >
              🔒 Exclusión Mutua
              <span className="block text-xs text-purple-300 mt-0.5">3 vehículos → misma intersección</span>
            </button>
            <button
              onClick={() => handleScenario("priority_demo")}
              className="w-full px-3 py-2.5 bg-yellow-600 hover:bg-yellow-700 rounded text-sm font-medium"
            >
              🚑 Priority Scheduling
              <span className="block text-xs text-yellow-300 mt-0.5">Ambulancia P0 gana a normales P2</span>
            </button>
            <button
              onClick={() => handleScenario("deadlock_demo")}
              className="w-full px-3 py-2.5 bg-red-700 hover:bg-red-800 rounded text-sm font-medium"
            >
              💀 Deadlock + Rollback
              <span className="block text-xs text-red-300 mt-0.5">2 vehículos → interbloqueo → auto-resolución</span>
            </button>
          </div>
        )}

        {/* TAB: Semáforos */}
        {activeTab === "config" && (
          <div className="space-y-3">
            <select
              value={selectedIntersection}
              onChange={(e) => setSelectedIntersection(e.target.value)}
              className="w-full bg-gray-600 p-2 rounded text-sm text-white"
            >
              <option value="">Seleccionar intersección...</option>
              {intersections.map(i => (
                <option key={i.id} value={i.id}>{i.id}</option>
              ))}
            </select>

            <div>
              <label className="text-xs text-gray-400">🟢 Verde: {greenTime}s</label>
              <input type="range" min="3" max="30" value={greenTime}
                onChange={(e) => setGreenTime(Number(e.target.value))} className="w-full" />
            </div>
            <div>
              <label className="text-xs text-gray-400">🔴 Rojo: {redTime}s</label>
              <input type="range" min="3" max="30" value={redTime}
                onChange={(e) => setRedTime(Number(e.target.value))} className="w-full" />
            </div>
            <button
              onClick={handleUpdateTiming}
              disabled={!selectedIntersection || loading}
              className="w-full bg-blue-600 hover:bg-blue-700 p-2 rounded text-sm disabled:opacity-50"
            >
              Actualizar Tiempos
            </button>

            <div className="border-t border-gray-700 pt-3">
              <p className="text-xs text-gray-500 mb-2">Simular fallo manual:</p>
              <div className="grid grid-cols-3 gap-1.5">
                {intersections.map(i => (
                  <button key={i.id} onClick={() => handleTriggerFault(i.id)}
                    className="px-2 py-1.5 bg-red-600/40 hover:bg-red-600 rounded text-xs">
                    {i.id.split("_").slice(1).join(",")}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

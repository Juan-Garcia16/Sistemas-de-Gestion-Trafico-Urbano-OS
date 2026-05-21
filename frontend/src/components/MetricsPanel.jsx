import { useState } from "react";

export function MetricsPanel({ intersections, vehicles }) {
  const [collapsed, setCollapsed] = useState(false);

  if (collapsed) {
    return (
      <div className="bg-gray-800 p-2 rounded-lg text-white cursor-pointer"
        onClick={() => setCollapsed(false)}>
        <span className="text-sm">📊 Métricas SO ▸</span>
      </div>
    );
  }

  return (
    <div className="bg-gray-800 p-4 rounded-lg text-white text-xs">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-sm font-bold">📊 Métricas SO</h2>
        <button onClick={() => setCollapsed(true)} className="text-gray-400 hover:text-white">◂</button>
      </div>

      {/* Mutex / Exclusión Mutua */}
      <div className="mb-3">
        <h3 className="text-gray-400 font-semibold mb-1">🔒 Exclusión Mutua</h3>
        <div className="space-y-1 max-h-32 overflow-y-auto">
          {intersections.map(inter => (
            <div key={inter.id} className="flex items-center justify-between bg-gray-700/50 rounded px-2 py-1">
              <span className="text-gray-300 truncate w-20">{inter.id.split("_").slice(1).join(",")}</span>
              {inter.mutex_locked ? (
                <span className="text-red-400 flex items-center gap-1">
                  🔒 <span className="truncate max-w-16">{inter.mutex_owner || "?"}</span>
                </span>
              ) : (
                <span className="text-green-400">🟢 libre</span>
              )}
              <span className="text-gray-500">cola: {inter.queue_size || 0}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Vehículos en espera */}
      <div className="mb-3">
        <h3 className="text-gray-400 font-semibold mb-1">🚗 Vehículos ({vehicles.length})</h3>
        <div className="space-y-1 max-h-40 overflow-y-auto">
          {vehicles.filter(v => v.status !== "DONE").map(v => (
            <div key={v.id} className="flex items-center justify-between bg-gray-700/50 rounded px-2 py-1">
              <span className="truncate max-w-20 text-gray-300">{v.id}</span>
              <span className={`px-1 rounded text-xs ${
                v.priority === "EMERGENCY" ? "bg-red-600/50 text-red-300" :
                v.priority === "HIGH" ? "bg-yellow-600/50 text-yellow-300" :
                "bg-blue-600/50 text-blue-300"
              }`}>{v.priority}</span>
              <span className={`${
                v.status === "WAITING" ? "text-yellow-400" :
                v.status === "MOVING" ? "text-green-400" :
                "text-gray-500"
              }`}>{v.status}</span>
              {v.wait_time_ticks > 0 && (
                <span className="text-gray-500">{v.wait_time_ticks}t</span>
              )}
            </div>
          ))}
          {vehicles.filter(v => v.status !== "DONE").length === 0 && (
            <p className="text-gray-600 text-center py-2">Sin vehículos activos</p>
          )}
        </div>
      </div>

      {/* Leyenda */}
      <div className="text-gray-600 text-xs space-y-0.5 border-t border-gray-700 pt-2">
        <p>🔒 = mutex ocupado (exclusión mutua)</p>
        <p>cola = vehículos en espera</p>
        <p>t = ticks de espera</p>
      </div>
    </div>
  );
}

import { useState } from "react";

export function MetricsPanel({ intersections, vehicles }) {
  const [collapsed, setCollapsed] = useState(false);

  if (collapsed) {
    return (
      <div 
        className="bg-gray-800 p-3 rounded-lg text-white cursor-pointer flex items-center justify-between border border-gray-700 hover:border-gray-600 transition duration-200"
        onClick={() => setCollapsed(false)}
      >
        <span className="text-xs font-semibold uppercase tracking-wider text-gray-400">Diagnóstico SO</span>
        <span className="text-xs text-blue-400 font-bold">Mostrar [▸]</span>
      </div>
    );
  }

  // Ordenar intersecciones por coordenadas reales
  const getCoords = (i) => {
    if (i.position) return i.position;
    const parts = i.id.split("_");
    return { x: parseInt(parts[1]) || 0, y: parseInt(parts[2]) || 0 };
  };

  const sortedIntersections = [...intersections].sort((a, b) => {
    const posA = getCoords(a);
    const posB = getCoords(b);
    if (posA.y !== posB.y) return posA.y - posB.y;
    return posA.x - posB.x;
  });

  return (
    <div className="bg-gray-800/95 backdrop-blur-md p-4 rounded-lg text-white text-xs border border-gray-700 shadow-2xl flex flex-col gap-4 overflow-x-hidden">
      <div className="flex items-center justify-between border-b border-gray-700 pb-2">
        <div className="flex flex-col">
          <h2 className="text-xs font-bold uppercase tracking-wider text-gray-300">Monitor de Kernel / Recursos</h2>
          <span className="text-[10px] text-gray-500 font-mono">Tabla de Asignación de Recursos (RAG)</span>
        </div>
        <button 
          onClick={() => setCollapsed(true)} 
          className="text-gray-400 hover:text-white cursor-pointer px-2 py-0.5 rounded hover:bg-gray-700/50 transition duration-200"
          title="Colapsar panel"
        >
          [◂]
        </button>
      </div>

      {/* Sección 1: Mutexes / Exclusión Mutua */}
      <div>
        <div className="flex items-center justify-between mb-1.5">
          <h3 className="text-gray-400 font-bold uppercase text-[10px] tracking-wider">Sección Crítica (Mutexes)</h3>
          <span className="text-[10px] text-gray-500 font-mono">Primitivas P/V</span>
        </div>
        
        {/* Encabezado fijo de Mutexes */}
        <div className="grid grid-cols-[1.5fr_1.5fr_1.5fr_1fr] gap-2 px-2 py-1 bg-gray-900/60 rounded-t text-[10px] text-gray-400 font-semibold uppercase tracking-wider border-b border-gray-700 overflow-x-hidden">
          <div>Recurso</div>
          <div>Luz</div>
          <div>Propietario</div>
          <div className="text-right">Cola</div>
        </div>

        {/* Cuerpo de la tabla de Mutexes */}
        <div className="space-y-0.5 max-h-36 overflow-y-auto border-x border-b border-gray-900/40 rounded-b">
          {sortedIntersections.map(inter => {
            const coords = getCoords(inter);
            const isFault = inter.state === "FAULT";
            return (
              <div 
                key={inter.id} 
                className="grid grid-cols-[1.5fr_1.5fr_1.5fr_1fr] gap-2 px-2 py-1.5 bg-gray-700/20 hover:bg-gray-700/40 border-b border-gray-800/40 items-center transition duration-150 overflow-x-hidden"
              >
                {/* ID Recurso */}
                <span className="font-mono text-gray-300 font-bold">[{coords.x},{coords.y}]</span>
                
                {/* Estado del Semáforo */}
                <div>
                  <span className={`inline-flex items-center gap-1.5 px-1.5 py-0.5 rounded text-[10px] font-bold ${
                    isFault ? "bg-red-500/20 text-red-400 border border-red-500/30 animate-pulse" :
                    inter.state === "GREEN" ? "bg-green-500/10 text-green-400 border border-green-500/20" :
                    inter.state === "YELLOW" ? "bg-yellow-500/10 text-yellow-400 border border-yellow-500/20" :
                    "bg-red-500/10 text-red-400 border border-red-500/20"
                  }`}>
                    <span className={`w-1.5 h-1.5 rounded-full ${
                      isFault ? "bg-red-500 animate-ping" :
                      inter.state === "GREEN" ? "bg-green-500" :
                      inter.state === "YELLOW" ? "bg-yellow-500" :
                      "bg-red-500"
                    }`} />
                    {inter.state}
                  </span>
                </div>

                {/* Mutex Lock Propietario */}
                <div>
                  {inter.mutex_locked ? (
                    <span className="font-mono text-red-400 font-bold truncate block bg-red-950/20 px-1 py-0.5 rounded border border-red-900/30 text-[10px]">
                      LOCK: {inter.mutex_owner || "anon"}
                    </span>
                  ) : (
                    <span className="text-gray-500 text-[10px]">Libre</span>
                  )}
                </div>

                {/* Cola de Espera (Bloqueados) */}
                <div className="text-right font-mono">
                  {(inter.queue_size || 0) > 0 ? (
                    <span className="text-yellow-400 font-bold bg-yellow-950/20 px-1 py-0.5 rounded border border-yellow-900/30 text-[10px]">
                      {inter.queue_size}p
                    </span>
                  ) : (
                    <span className="text-gray-600">-</span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Sección 2: Tabla de Procesos (Vehículos) */}
      <div>
        <div className="flex items-center justify-between mb-1.5">
          <h3 className="text-gray-400 font-bold uppercase text-[10px] tracking-wider">Tabla de Procesos (Vehículos)</h3>
          <span className="text-[10px] text-gray-500 font-mono">Hilos Activos ({vehicles.length})</span>
        </div>

        {/* Encabezado de la tabla de Procesos */}
        <div className="grid grid-cols-[2fr_1.5fr_2.5fr_2fr_1fr] gap-2 px-2 py-1 bg-gray-900/60 rounded-t text-[10px] text-gray-400 font-semibold uppercase tracking-wider border-b border-gray-700 overflow-x-hidden">
          <div>ID Proceso</div>
          <div>Prio</div>
          <div>Ubicación / Ruta</div>
          <div>Estado</div>
          <div className="text-right">Visitas</div>
        </div>

        {/* Cuerpo de la tabla de Procesos */}
        <div className="space-y-0.5 max-h-48 overflow-y-auto border-x border-b border-gray-900/40 rounded-b">
          {vehicles.filter(v => v.status !== "DONE").map(v => {
            const locCoords = v.current_intersection ? getCoords({ id: v.current_intersection }) : null;
            return (
              <div 
                key={v.id} 
                className="grid grid-cols-[2fr_1.5fr_2.5fr_2fr_1fr] gap-2 px-2 py-1.5 bg-gray-700/20 hover:bg-gray-700/40 border-b border-gray-800/40 items-center transition duration-150 overflow-x-hidden"
              >
                {/* ID Proceso */}
                <span className="font-mono text-gray-300 font-semibold truncate" title={v.id}>{v.id}</span>
                
                {/* Prioridad */}
                <div>
                  <span className={`inline-block px-1 py-0.5 rounded font-mono text-[9px] font-bold ${
                    v.priority === "EMERGENCY" ? "bg-red-950 text-red-400 border border-red-900/40" :
                    v.priority === "HIGH" ? "bg-yellow-950 text-yellow-500 border border-yellow-900/40" :
                    "bg-blue-950 text-blue-400 border border-blue-900/40"
                  }`}>
                    {v.priority === "EMERGENCY" ? "P0" : v.priority === "HIGH" ? "P1" : "P2"}
                  </span>
                </div>

                {/* Ubicación / Ruta */}
                <span className="font-mono text-gray-400 text-[10px] truncate">
                  {locCoords ? `[${locCoords.x},${locCoords.y}]` : "-"}
                </span>

                {/* Estado del Proceso */}
                <div>
                  <span className={`inline-flex items-center gap-1 px-1 py-0.5 rounded font-mono text-[9px] font-bold ${
                    v.status === "WAITING" ? "bg-yellow-500/10 text-yellow-400 border border-yellow-500/20 animate-pulse" :
                    v.status === "MOVING" ? "bg-green-500/10 text-green-400 border border-green-500/20" :
                    "bg-gray-500/10 text-gray-500 border border-gray-500/20"
                  }`}>
                    <span className={`w-1 h-1 rounded-full ${
                      v.status === "WAITING" ? "bg-yellow-500 animate-ping" :
                      v.status === "MOVING" ? "bg-green-500" :
                      "bg-gray-500"
                    }`} />
                    {v.status}
                  </span>
                </div>

                {/* Pasos / Ticks de Visita */}
                <div className="text-right font-mono text-gray-400 text-[10px] font-bold">
                  {v.visited || 0}
                </div>
              </div>
            );
          })}
          {vehicles.filter(v => v.status !== "DONE").length === 0 && (
            <p className="text-gray-500 text-center py-4 font-mono">Sin procesos (hilos) activos</p>
          )}
        </div>
      </div>

      {/* Pie de página con leyenda descriptiva limpia */}
      <div className="grid grid-cols-2 gap-2 text-[10px] text-gray-500 font-mono border-t border-gray-700 pt-2 bg-gray-900/20 p-2 rounded">
        <div>LOCK: Mutex retenido por proceso</div>
        <div>P0/P1/P2: Jerarquía del Planificador</div>
        <div>Cola: Hilos bloqueados en recurso</div>
        <div>Pasos: Transiciones de sección crítica</div>
      </div>
    </div>
  );
}

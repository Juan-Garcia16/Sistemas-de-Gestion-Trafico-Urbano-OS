import { useRef } from "react";

const vehicleConfig = {
  EMERGENCY: { body: "#DC2626", roof: "#EF4444", width: 26, height: 14 },
  HIGH:      { body: "#F59E0B", roof: "#FBBF24", width: 28, height: 15 },
  NORMAL:    { body: "#3B82F6", roof: "#60A5FA", width: 22, height: 12 }
};

function CarSVG({ config }) {
  const w = config.width;
  const h = config.height;
  const r = h * 0.35;
  const roofW = w * 0.35;
  const roofH = h * 0.35;
  return (
    <svg width={w} height={h} viewBox={`0 0 ${w} ${h}`}>
      <rect x={r * 0.6} y={h * 0.15} width={w - r * 1.2} height={h * 0.65} rx={r} fill={config.body} />
      <rect x={w * 0.3} y={0} width={roofW} height={roofH} rx="2" fill={config.roof} />
      <circle cx={w * 0.25} cy={h * 0.78} r={r * 0.5} fill="#1F2937" />
      <circle cx={w * 0.75} cy={h * 0.78} r={r * 0.5} fill="#1F2937" />
    </svg>
  );
}

export function VehicleMarker({ id, status, priority, currentPosition, cellSize = 80 }) {
  const prevPosRef = useRef(null);
  const angleRef = useRef(0);

  if (prevPosRef.current === null) {
    prevPosRef.current = currentPosition;
  }

  const prev = prevPosRef.current;
  const dx = currentPosition.x - prev.x;
  const dy = currentPosition.y - prev.y;

  // Corregir el bug visual de rotación: sólo recalcular el ángulo si el vehículo realmente se movió.
  // Esto evita que gire repentinamente a 0 grados (apuntando a la derecha) al detenerse en un semáforo.
  if (dx !== 0 || dy !== 0) {
    angleRef.current = Math.atan2(dy, dx) * (180 / Math.PI);
  }

  prevPosRef.current = currentPosition;

  if (status === "DONE") return null;

  const cfg = vehicleConfig[priority] || vehicleConfig.NORMAL;
  const halfCell = cellSize / 2;

  // Colores y clases para anillos de diagnóstico de estado
  const isWaiting = status === "WAITING";
  const isMoving = status === "MOVING";
  
  let ringClass = "ring-2 ring-blue-500/30";
  if (isWaiting) {
    ringClass = "ring-2 ring-yellow-500 animate-pulse shadow-lg shadow-yellow-900/30";
  } else if (isMoving) {
    ringClass = "ring-2 ring-green-500 shadow-md shadow-green-950/40";
  }

  return (
    <div
      className={`absolute transition-all duration-700 ease-in-out flex flex-col items-center select-none`}
      style={{
        left: currentPosition.x * cellSize + halfCell,
        top: currentPosition.y * cellSize + halfCell,
        transform: `translate(-50%, -50%)`,
        zIndex: 15
      }}
    >
      {/* Etiqueta flotante con el ID real del proceso (Vehículo) para diagnóstico fácil */}
      <span className="text-[9px] font-mono font-bold bg-gray-950/90 text-gray-200 border border-gray-800/80 px-1 py-0.5 rounded shadow mb-1 tracking-tight truncate max-w-16 pointer-events-none">
        {id}
      </span>

      {/* Contenedor del coche con anillo de estado y rotación estable */}
      <div
        className={`p-1 rounded-full transition-all duration-300 ${ringClass}`}
        style={{
          transform: `rotate(${angleRef.current}deg)`,
          // Mantener opacidad alta (85%) en espera para permitir el diagnóstico visual
          opacity: isWaiting ? 0.85 : 1,
          backgroundColor: isWaiting ? "rgba(234, 179, 8, 0.05)" : "transparent"
        }}
        title={`${id} [${priority}] - ${status}`}
      >
        <CarSVG config={cfg} />
      </div>

      {/* Badge de prioridad (P0, P1, P2) */}
      <div className={`absolute -bottom-1 -right-1 text-xs rounded-full px-1 h-3 flex items-center justify-center font-mono font-bold border pointer-events-none
        ${priority === "EMERGENCY" ? "bg-red-950 text-red-400 border-red-900/40" : 
          priority === "HIGH" ? "bg-yellow-950 text-yellow-500 border-yellow-900/40" : 
          "bg-blue-950 text-blue-400 border-blue-900/40"}`}
        style={{ fontSize: '7px', minWidth: '12px' }}>
        {priority === "EMERGENCY" ? "P0" : priority === "HIGH" ? "P1" : "P2"}
      </div>
    </div>
  );
}
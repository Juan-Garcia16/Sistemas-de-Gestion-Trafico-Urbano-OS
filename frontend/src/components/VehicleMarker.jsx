import { useRef, useEffect } from "react";

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
      {/* Body */}
      <rect x={r * 0.6} y={h * 0.15} width={w - r * 1.2} height={h * 0.65} rx={r} fill={config.body} />
      {/* Roof */}
      <rect x={w * 0.3} y={0} width={roofW} height={roofH} rx="2" fill={config.roof} />
      {/* Left wheel */}
      <circle cx={w * 0.25} cy={h * 0.78} r={r * 0.5} fill="#1F2937" />
      {/* Right wheel */}
      <circle cx={w * 0.75} cy={h * 0.78} r={r * 0.5} fill="#1F2937" />
      {/* Emergency cross for EMERGENCY vehicles */}
      {config === vehicleConfig.EMERGENCY && (
        <g transform={`translate(${w * 0.48}, ${h * 0.4})`}>
          <rect x="-3" y="-1" width="6" height="2" fill="white" rx="0.5" />
          <rect x="-1" y="-3" width="2" height="6" fill="white" rx="0.5" />
        </g>
      )}
    </svg>
  );
}

export function VehicleMarker({ id, status, priority, currentPosition, cellSize = 80 }) {
  const prevPos = useRef(currentPosition);

  useEffect(() => {
    prevPos.current = currentPosition;
  }, [currentPosition]);

  if (status === "DONE") return null;

  const cfg = vehicleConfig[priority] || vehicleConfig.NORMAL;
  const prev = prevPos.current || currentPosition;
  const halfCell = cellSize / 2;

  const dx = currentPosition.x - prev.x;
  const dy = currentPosition.y - prev.y;
  const angle = Math.atan2(dy, dx) * (180 / Math.PI);

  return (
    <div
      className={`absolute transition-all duration-700 ease-in-out ${
        status === "WAITING" ? "opacity-40 scale-90" : "opacity-100 scale-100"
      } ${status === "BLOCKED" ? "grayscale" : ""}`}
      style={{
        left: currentPosition.x * cellSize + halfCell,
        top: currentPosition.y * cellSize + halfCell,
        transform: `translate(-50%, -50%) rotate(${angle}deg)`,
        filter: status !== "WAITING" ? "drop-shadow(0 2px 3px rgba(0,0,0,0.5))" : "none",
        zIndex: 10
      }}
      title={`${id} (${priority}) - ${status}`}
    >
      <CarSVG config={cfg} />
      <div className={`absolute -top-3 -right-2 text-xs rounded-full px-1 h-4 flex items-center justify-center font-bold
        ${priority === "EMERGENCY" ? "bg-red-600 text-white" : 
          priority === "HIGH" ? "bg-yellow-500 text-black" : 
          "bg-blue-500 text-white"}`}
        style={{ fontSize: '8px', minWidth: '14px' }}>
        {priority === "EMERGENCY" ? "P0" : priority === "HIGH" ? "P1" : "P2"}
      </div>
    </div>
  );
}

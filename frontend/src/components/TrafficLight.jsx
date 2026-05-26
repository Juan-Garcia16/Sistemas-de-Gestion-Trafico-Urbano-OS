export function TrafficLight({ id, state, position, cellSize = 80 }) {
  // Ajustar la proporción para que el semáforo sea visible e imponente en el mapa
  const lightColors = {
    RED: "#EF4444",
    GREEN: "#22C55E",
    YELLOW: "#EAB308"
  };

  const isActive = (color) => state === color;
  const isFault = state === "FAULT";

  const lightStyle = (color) => ({
    backgroundColor: isFault ? "#6B7280" : lightColors[color],
    opacity: isFault ? 0.35 : isActive(color) ? 1 : 0.12,
    boxShadow: isActive(color) && !isFault ? `0 0 20px 4px ${lightColors[color]}, inset 0 0 8px rgba(255,255,255,0.4)` : "none"
  });

  // Coordenadas legibles
  const parts = id.split("_");
  const label = `[${parts[1]},${parts[2]}]`;

  return (
    <div
      className="absolute flex flex-col items-center select-none"
      style={{
        left: position.x * cellSize + 50,
        top: position.y * cellSize + 20,
        transform: "translate(-25%, -25%)"
      }}
    >
      {/* Housing (Caja del Semáforo) */}
      <div className={`bg-gray-900 border-2 border-gray-700/60 rounded-xl shadow-2xl p-1.5 flex flex-col gap-1.5 relative ${isFault ? "traffic-light-fault" : ""
        }`}>
        {/* Luz Roja */}
        <div
          className={`rounded-full transition-all duration-300 ${isActive("RED") ? "traffic-light-active" : ""}`}
          style={{
            ...lightStyle("RED"),
            width: "8px",
            height: "8px",
            border: "1px solid rgba(0,0,0,0.5)"
          }}
          title="Fase: Alto"
        />
        {/* Luz Amarilla */}
        <div
          className={`rounded-full transition-all duration-300 ${isActive("YELLOW") ? "traffic-light-active" : ""}`}
          style={{
            ...lightStyle("YELLOW"),
            width: "8px",
            height: "8px",
            border: "1px solid rgba(0,0,0,0.5)"
          }}
          title="Fase: Transición"
        />
        {/* Luz Verde */}
        <div
          className={`rounded-full transition-all duration-300 ${isActive("GREEN") ? "traffic-light-active" : ""}`}
          style={{
            ...lightStyle("GREEN"),
            width: "8px",
            height: "8px",
            border: "1px solid rgba(0,0,0,0.5)"
          }}
          title="Fase: Marcha"
        />
      </div>

      {/* Poste del semáforo con degradado metálico */}
      <div className="w-1.5 h-3 bg-gradient-to-r from-gray-700 via-gray-600 to-gray-800 shadow" />

      {/* Base de soporte */}
      <div className="w-4 h-0.5 bg-gray-700 rounded shadow" />

      {/* Etiqueta de la Intersección (Coordenadas) */}
      <span className="text-[10px] font-mono font-bold text-gray-400 bg-gray-950/70 border border-gray-800/80 px-1 rounded shadow-sm mt-1 select-none pointer-events-none">
        {label}
      </span>
    </div>
  );
}

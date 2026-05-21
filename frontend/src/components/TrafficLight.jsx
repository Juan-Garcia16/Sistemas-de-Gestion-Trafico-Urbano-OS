export function TrafficLight({ id, state, position, cellSize = 80 }) {
  const scale = cellSize / 80;
  const lightColors = {
    RED: "#EF4444",
    GREEN: "#22C55E",
    YELLOW: "#EAB308"
  };

  const isActive = (color) => state === color;
  const isFault = state === "FAULT";

  const lightStyle = (color) => ({
    backgroundColor: isFault ? "#6B7280" : lightColors[color],
    opacity: isFault ? 0.5 : isActive(color) ? 1 : 0.15,
    boxShadow: isActive(color) && !isFault ? `0 0 ${12 * scale}px ${lightColors[color]}` : "none"
  });

  return (
    <div
      className="absolute flex flex-col items-center"
      style={{ left: position.x * cellSize, top: position.y * cellSize }}
    >
      {/* Housing */}
      <div className={`bg-gray-800 rounded-lg border border-gray-600 shadow-lg ${
        isFault ? "traffic-light-fault" : ""
      }`}
        style={{ padding: `${1.5 * scale}px` }}
      >
        <div
          className={`rounded-full mb-1 ${isActive("RED") ? "traffic-light-active" : ""}`}
          style={{
            ...lightStyle("RED"),
            width: `${4 * scale}px`,
            height: `${4 * scale}px`
          }}
        />
        <div
          className={`rounded-full mb-1 ${isActive("YELLOW") ? "traffic-light-active" : ""}`}
          style={{
            ...lightStyle("YELLOW"),
            width: `${4 * scale}px`,
            height: `${4 * scale}px`
          }}
        />
        <div
          className={`rounded-full ${isActive("GREEN") ? "traffic-light-active" : ""}`}
          style={{
            ...lightStyle("GREEN"),
            width: `${4 * scale}px`,
            height: `${4 * scale}px`
          }}
        />
      </div>
      {/* Pole */}
      <div style={{ width: `${1.5 * scale}px`, height: `${5 * scale}px` }} className="bg-gray-600" />
      {/* Base */}
      <div style={{ width: `${3 * scale}px`, height: `${1 * scale}px` }} className="bg-gray-500 rounded" />
      {/* Label */}
      <span className="text-xs text-gray-400 mt-1">{id}</span>
    </div>
  );
}

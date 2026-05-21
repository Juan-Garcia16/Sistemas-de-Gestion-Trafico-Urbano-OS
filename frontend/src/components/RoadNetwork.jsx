export function RoadNetwork({ intersections, cellSize = 80 }) {
  const positions = {};
  intersections.forEach(i => { positions[i.id] = i.position; });

  const edgeSet = new Set();
  const roads = [];

  intersections.forEach(i => {
    const { x, y } = i.position;
    const neighbors = [
      { dx: 1, dy: 0 },
      { dx: 0, dy: 1 }
    ];
    neighbors.forEach(({ dx, dy }) => {
      const nx = x + dx;
      const ny = y + dy;
      const neighborId = `intersection_${nx}_${ny}`;
      if (positions[neighborId]) {
        const key = [i.id, neighborId].sort().join("-");
        if (!edgeSet.has(key)) {
          edgeSet.add(key);
          roads.push({ from: i.position, to: positions[neighborId] });
        }
      }
    });
  });

  const cx = (p) => p.x * cellSize + cellSize / 2;
  const cy = (p) => p.y * cellSize + cellSize / 2;
  const total = 3 * cellSize;

  return (
    <svg
      className="absolute top-0 left-0"
      width={total}
      height={total}
      style={{ zIndex: 0 }}
    >
      {roads.map(({ from, to }, idx) => (
        <g key={idx}>
          {/* Road surface */}
          <line
            x1={cx(from)} y1={cy(from)} x2={cx(to)} y2={cy(to)}
            stroke="#1F2937" strokeWidth="24" strokeLinecap="butt"
          />
          {/* Road edges */}
          <line
            x1={cx(from)} y1={cy(from)} x2={cx(to)} y2={cy(to)}
            stroke="#374151" strokeWidth="20" strokeLinecap="butt"
          />
          {/* Center dashed line */}
          <line
            x1={cx(from)} y1={cy(from)} x2={cx(to)} y2={cy(to)}
            stroke="#6B7280" strokeWidth="1" strokeDasharray="4,4" strokeLinecap="butt"
          />
        </g>
      ))}
      {/* Crosswalks at each intersection */}
      {intersections.map(i => {
        const { x, y } = i.position;
        const centerX = cx({ x, y });
        const centerY = cy({ x, y });
        return (
          <g key={`cw-${i.id}`}>
            {[-4, -2, 0, 2, 4].map(offset => (
              <line key={offset}
                x1={centerX + offset} y1={centerY - 10}
                x2={centerX + offset} y2={centerY + 10}
                stroke="#9CA3AF" strokeWidth="1" opacity="0.5"
              />
            ))}
          </g>
        );
      })}
    </svg>
  );
}

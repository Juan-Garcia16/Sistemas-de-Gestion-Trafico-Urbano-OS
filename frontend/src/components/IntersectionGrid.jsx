import { TrafficLight } from "./TrafficLight";
import { VehicleMarker } from "./VehicleMarker";
import { RoadNetwork } from "./RoadNetwork";

const CELL_SIZE = 180;
const COLS = 3;

export function IntersectionGrid({ intersections, vehicles }) {
  const total = COLS * CELL_SIZE;
  const padding = 32;

  return (
    <div
      className="relative bg-gray-950 rounded-xl border border-gray-800 overflow-hidden"
      style={{
        width: total + padding * 2,
        height: total + padding * 2,
        maxWidth: "100%"
      }}
    >
      {/* Road network layer (bottom) */}
      <div className="absolute" style={{ left: padding / 2, top: padding / 2 }}>
        <RoadNetwork intersections={intersections} cellSize={CELL_SIZE} />
      </div>

      {/* Traffic lights layer (middle) */}
      <div className="absolute" style={{ left: padding / 2, top: padding / 2, zIndex: 5 }}>
        {intersections.map(intersection => (
          <TrafficLight
            key={intersection.id}
            id={intersection.id}
            state={intersection.state}
            position={intersection.position}
            cellSize={CELL_SIZE}
          />
        ))}
        {/* Overlays: lock + queue badge + fault */}
        {intersections.map(intersection => {
          const x = intersection.position.x * CELL_SIZE;
          const y = intersection.position.y * CELL_SIZE;
          return (
            <div key={`overlay-${intersection.id}`} className="absolute" style={{ left: x, top: y, pointerEvents: 'none' }}>
              {/* Fault overlay */}
              {intersection.state === "FAULT" && (
                <div className="absolute -inset-2 bg-red-600/30 rounded-lg animate-pulse border-2 border-red-500"
                  style={{ width: CELL_SIZE, height: CELL_SIZE }} />
              )}
              {/* Lock badge */}
              {intersection.mutex_locked && (
                <div className="absolute top-0 right-0 bg-red-600 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center font-bold"
                  style={{ transform: 'translate(8px, -8px)', zIndex: 15 }}
                  title={`Mutex tomado por: ${intersection.mutex_owner || 'desconocido'}`}
                >
                  🔒
                </div>
              )}
              {/* Queue badge */}
              {(intersection.queue_size || 0) > 0 && (
                <div className="absolute bottom-0 left-0 bg-yellow-600 text-white text-xs rounded-full px-1.5 h-5 flex items-center justify-center font-bold"
                  style={{ transform: 'translate(-8px, 8px)', zIndex: 15 }}
                  title={`${intersection.queue_size} vehículos en cola`}
                >
                  {intersection.queue_size}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Vehicles layer (top) */}
      <div className="absolute pointer-events-none" style={{ left: padding / 2, top: padding / 2, zIndex: 10 }}>
        {vehicles.map(v => (
          <VehicleMarker
            key={v.id}
            id={v.id}
            status={v.status}
            priority={v.priority}
            currentPosition={v.currentPosition}
            route={v.route}
            cellSize={CELL_SIZE}
          />
        ))}
      </div>
    </div>
  );
}

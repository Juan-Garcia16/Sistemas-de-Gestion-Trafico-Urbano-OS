from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid

from auth.roles import require_role, require_any_role
from core.vehicle import Priority
from simulation.engine import SimulationEngine
from simulation.network import IntersectionNetwork
from core.scheduler import TrafficScheduler
from api.websocket import manager

# Engine y red globales (compartidas entre rutas y para broadcast)
_engine: SimulationEngine | None = None
_network: IntersectionNetwork | None = None
_scheduler: TrafficScheduler | None = None

router = APIRouter(prefix="/simulation", tags=["Simulation"])


class AddVehicleRequest(BaseModel):
    """Modelo para el body de POST /simulation/vehicle"""
    id: str
    route: list
    priority: str


def get_engine() -> SimulationEngine:
    """Helper para obtener el engine activo o lanzar error."""
    if _engine is None:
        raise HTTPException(status_code=400, detail="Simulación no iniciada")
    return _engine


@router.post("/start")
def start_simulation(user=Depends(require_role("control"))):
    """
    Inicia la simulación del sistema de tráfico.
    Crea la red de intersecciones, el scheduler y el motor de simulación.
    Requiere rol 'control'.
    """
    global _engine, _network, _scheduler

    if _engine is not None and _engine._tick_thread is not None and _engine._tick_thread.is_alive():
        raise HTTPException(status_code=400, detail="Simulación ya está corriendo")

    # Crear red de intersecciones (3x3 grid)
    _network = IntersectionNetwork()
    for i in range(3):
        for j in range(3):
            _network.add_intersection(f"intersection_{i}_{j}")

    # Conectar intersecciones en grid
    for i in range(3):
        for j in range(3):
            if i < 2:
                _network.connect(f"intersection_{i}_{j}", f"intersection_{i+1}_{j}")
            if j < 2:
                _network.connect(f"intersection_{i}_{j}", f"intersection_{i}_{j+1}")

    # Crear scheduler
    _scheduler = TrafficScheduler()

    # Función de broadcast vía WebSocket
    async def broadcast_state(state):
        await manager.broadcast(state)

    # Crear engine con la función de broadcast
    _engine = SimulationEngine(_network, _scheduler, broadcast_func=broadcast_state)
    _engine.start()

    return {
        "status": "started",
        "intersections": len(_network.nodes)
    }


@router.post("/stop")
def stop_simulation(user=Depends(require_role("control"))):
    """
    Detiene la simulación en curso.
    Requiere rol 'control'.
    """
    global _engine

    if _engine is None:
        raise HTTPException(status_code=400, detail="No hay simulación activa")

    _engine.stop()
    _engine = None

    return {"status": "stopped"}


@router.get("/status")
def get_status(user=Depends(require_any_role("viewer", "control"))):
    """
    Obtiene el estado actual de la simulación.
    Incluye estado de intersecciones, vehículos y ticks.
    Requiere rol 'viewer' o 'control'.
    """
    if _engine is None:
        return {
            "running": False,
            "tick": 0,
            "intersections": [],
            "vehicles": []
        }

    snapshot = _engine.state_snapshot()

    return {
        "running": _engine._tick_thread is not None and _engine._tick_thread.is_alive(),
        "tick": snapshot.get("tick", 0),
        "intersections": [
            {
                "id": inter["id"],
                "state": inter["state"],
                "position": {"x": int(inter["id"].split("_")[1]), "y": int(inter["id"].split("_")[2])},
                "vehicle_count": 0
            }
            for inter in snapshot.get("intersections", [])
        ],
        "vehicles": [
            {
                "id": v["id"],
                "status": v["status"],
                "position": v["position"],
                "route": [],  # El Vehicle no expone route fácilmente
                "priority": "NORMAL"
            }
            for v in snapshot.get("vehicles", [])
        ]
    }


@router.post("/vehicle")
def add_vehicle(request: AddVehicleRequest, user=Depends(require_role("control"))):
    """
    Agrega un vehículo a la simulación en ejecución.
    Requiere rol 'control'.
    """
    engine = get_engine()

    # Mapear string priority a Priority enum
    if request.priority == "EMERGENCY":
        p = Priority.EMERGENCY
    elif request.priority == "HIGH":
        p = Priority.HIGH
    else:
        p = Priority.NORMAL

    engine.add_vehicle(request.id, request.route, p)

    return {"status": "vehicle_added", "vehicle_id": request.id}
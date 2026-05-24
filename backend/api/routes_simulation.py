from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid

from auth.roles import require_role, require_any_role
from core.vehicle import Priority
from simulation.engine import SimulationEngine
from simulation.network import IntersectionNetwork
from config import TRAFFIC_LIGHT_DEFAULT_GREEN, TRAFFIC_LIGHT_DEFAULT_RED
from core.intersection import Intersection
from core.scheduler import TrafficScheduler
from api.websocket import manager
from core.fault_handler import FaultHandler
from core.deadlock_detector import DeadlockDetector
from db.database import SessionLocal
from db.models import EventLog
from datetime import datetime

# Engine y red globales (compartidas entre rutas y para broadcast)
_engine: SimulationEngine | None = None
_network: IntersectionNetwork | None = None
_scheduler: TrafficScheduler | None = None
_fault_handler: FaultHandler | None = None
_deadlock_detector: DeadlockDetector | None = None

def _intersection_coords(inter_id: str) -> dict:
    """Deriva coordenadas {x, y} del id de intersección (formato: intersection_i_j)."""
    parts = inter_id.split("_")
    return {"x": int(parts[1]), "y": int(parts[2])}


router = APIRouter(prefix="/simulation", tags=["Simulation"])


class AddVehicleRequest(BaseModel):
    """Modelo para el body de POST /simulation/vehicle"""
    id: str
    route: list
    priority: str


class ScenarioRequest(BaseModel):
    """Modelo para el body de POST /simulation/scenario"""
    scenario: str  # "mutex_demo" | "priority_demo" | "deadlock_demo"


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

    # --- FaultHandler: fallos aleatorios con broadcast y log ---
    global _fault_handler, _deadlock_detector

    async def broadcast_event(event_data: dict):
        await manager.broadcast(event_data)

    def on_fault(intersection_id: str):
        timestamp = datetime.utcnow().isoformat()
        db = SessionLocal()
        try:
            log = EventLog(timestamp=timestamp, event_type="FAULT", intersection_id=intersection_id, details='{"source": "fault_handler"}')
            db.add(log)
            db.commit()
        finally:
            db.close()

    def on_restore(intersection_id: str):
        pass

    _fault_handler = FaultHandler(_network, on_fault, on_restore)
    _fault_handler.start()

    # --- DeadlockDetector: detección de interbloqueos ---
    def on_deadlock(vehicle_id: str, intersection_id: str):
        timestamp = datetime.utcnow().isoformat()
        _scheduler.remove_vehicle(vehicle_id)
        async def send():
            await manager.broadcast({
                "type": "DEADLOCK",
                "vehicle_id": vehicle_id,
                "intersection_id": intersection_id,
                "timestamp": timestamp
            })
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send())
        loop.close()
        db = SessionLocal()
        try:
            log = EventLog(timestamp=timestamp, event_type="DEADLOCK", vehicle_id=vehicle_id, intersection_id=intersection_id, details='{"resolution": "rollback_vehicle_removed"}')
            db.add(log)
            db.commit()
        finally:
            db.close()

    _deadlock_detector = DeadlockDetector(_scheduler, on_deadlock)
    _deadlock_detector.start()

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
    global _engine, _fault_handler, _deadlock_detector

    if _fault_handler:
        _fault_handler.stop()
        _fault_handler = None

    if _deadlock_detector:
        _deadlock_detector.stop()
        _deadlock_detector = None

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
        return {"running": False, "tick": 0, "intersections": [], "vehicles": []}

    snapshot = _engine.state_snapshot()

    # Contar vehículos por intersección
    vehicle_counts = {}
    for v in snapshot.get("vehicles", []):
        inter_id = v.get("current_intersection", "")
        if inter_id:
            vehicle_counts[inter_id] = vehicle_counts.get(inter_id, 0) + 1

    return {
        "running": _engine._tick_thread is not None and _engine._tick_thread.is_alive(),
        "tick": snapshot.get("tick", 0),
        "intersections": [
            {
                "id": inter["id"],
                "state": inter["state"],
                "position": inter.get("position", _intersection_coords(inter["id"])),
                "vehicle_count": vehicle_counts.get(inter["id"], 0)
            }
            for inter in snapshot.get("intersections", [])
        ],
        "vehicles": [
            {
                "id": v["id"],
                "status": v["status"],
                "position": v["position"],
                "route": v.get("route", []),
                "priority": v.get("priority", "NORMAL"),
                "currentPosition": v.get("currentPosition", _intersection_coords(v.get("current_intersection", "intersection_0_0")))
            }
            for v in snapshot.get("vehicles", [])
        ]
    }




@router.get("/metrics")
def get_metrics(user=Depends(require_any_role("viewer", "control"))):
    """
    Métricas en tiempo real de conceptos de SO:
    - Estado del mutex por intersección
    - Tamaño de colas
    - Vehículos en espera con tiempos
    - Deadlocks detectados
    """
    if _engine is None:
        return {
            "tick": 0,
            "intersections": [],
            "vehicles": [],
            "deadlocks_detected": 0
        }

    snapshot = _engine.state_snapshot()

    return {
        "tick": snapshot.get("tick", 0),
        "intersections": [
            {
                "id": inter["id"],
                "state": inter["state"],
                "queue_size": inter.get("queue_size", 0),
                "queued_vehicles": inter.get("queued_vehicles", []),
                "mutex_owner": inter.get("mutex_owner"),
                "mutex_locked": inter.get("mutex_locked", False)
            }
            for inter in snapshot.get("intersections", [])
        ],
        "vehicles": [
            {
                "id": v["id"],
                "priority": v.get("priority", "NORMAL"),
                "status": v["status"],
                "current_intersection": v.get("current_intersection", ""),
                "wait_time_ticks": v.get("wait_time_ticks", 0)
            }
            for v in snapshot.get("vehicles", [])
        ],
        "deadlocks_detected": 0
    }


@router.post("/scenario")
def run_scenario(request: ScenarioRequest, user=Depends(require_role("control"))):
    """
    Ejecuta un escenario predefinido para demostrar un concepto de SO.
    
    Escenarios disponibles:
    - mutex_demo: 3 vehículos normales compiten por la misma intersección
    - priority_demo: 1 ambulancia + 2 normales → ambulancia gana por prioridad
    - deadlock_demo: 2 vehículos con rutas que generan interbloqueo
    """
    engine = get_engine()
    scenario = request.scenario
    vehicles_added = []

    if scenario == "mutex_demo":
        # 3 vehículos normales → intersection_1_1
        route = ["intersection_0_0", "intersection_1_0", "intersection_1_1"]
        for i in range(3):
            vid = f"mutex-car-{i+1}"
            engine.add_vehicle(vid, route.copy(), Priority.NORMAL)
            vehicles_added.append(vid)

    elif scenario == "priority_demo":
        # 2 normales primero, luego 1 ambulancia → ambulancia debe pasar primero
        route = ["intersection_0_0", "intersection_0_1", "intersection_0_2"]
        engine.add_vehicle("normal-1", route.copy(), Priority.NORMAL)
        engine.add_vehicle("normal-2", route.copy(), Priority.NORMAL)
        engine.add_vehicle("ambulancia-prio", route.copy(), Priority.EMERGENCY)
        vehicles_added = ["normal-1", "normal-2", "ambulancia-prio"]

    elif scenario == "deadlock_demo":
        # Dos vehículos con rutas que se cruzan → deadlock
        route_a = ["intersection_0_0", "intersection_1_0", "intersection_1_1", "intersection_1_2"]
        route_b = ["intersection_1_1", "intersection_1_0", "intersection_0_0", "intersection_0_1"]
        engine.add_vehicle("deadlock-A", route_a, Priority.NORMAL)
        engine.add_vehicle("deadlock-B", route_b, Priority.NORMAL)
        vehicles_added = ["deadlock-A", "deadlock-B"]

    else:
        raise HTTPException(status_code=400, detail=f"Escenario desconocido: {scenario}. Use: mutex_demo, priority_demo, deadlock_demo")

    return {
        "status": "scenario_executed",
        "scenario": scenario,
        "vehicles_added": vehicles_added,
        "description": {
            "mutex_demo": "Exclusión Mutua: 3 vehículos compiten por la misma intersección. Solo 1 pasa a la vez.",
            "priority_demo": "Priority Scheduling: 1 ambulancia (prio=0) + 2 normales (prio=2). La ambulancia pasa primero.",
            "deadlock_demo": "Detección de Deadlock: 2 vehículos con rutas que generan interbloqueo. Timeout >10s → rollback."
        }.get(scenario, "")
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
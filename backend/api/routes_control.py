from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from auth.roles import require_role
from db.database import get_db
from db.models import EventLog, LightConfig

# Engine y network globales (para modificar en tiempo real)
from api.routes_simulation import get_engine

router = APIRouter(prefix="/control", tags=["Control"])


class UpdateTimingRequest(BaseModel):
    """Modelo para el body de PUT /control/lights/{id}/timing"""
    green_time: int
    red_time: int


@router.put("/lights/{intersection_id}/timing")
def update_timing(
    intersection_id: str,
    request: UpdateTimingRequest,
    db: Session = Depends(get_db),
    user=Depends(require_role("control"))
):
    """
    Actualiza los tiempos de verde y rojo de un semáforo.
    Los cambios se persisten en la base de datos y se aplican en tiempo real.
    Requiere rol 'control'.
    """
    green_time = request.green_time
    red_time = request.red_time

    engine = get_engine()

    # Buscar intersección en la red
    network = engine.network
    if intersection_id not in network.nodes:
        raise HTTPException(status_code=404, detail="Intersección no encontrada")

    intersection = network.nodes[intersection_id]

    # Actualizar tiempos del semáforo
    intersection.light.green_time = green_time
    intersection.light.red_time = red_time

    # Guardar o actualizar en DB
    config = db.query(LightConfig).filter(LightConfig.intersection_id == intersection_id).first()
    if config:
        config.green_time = green_time
        config.red_time = red_time
        config.updated_by = user.get("sub")
        config.updated_at = datetime.utcnow().isoformat()
    else:
        config = LightConfig(
            intersection_id=intersection_id,
            green_time=green_time,
            red_time=red_time,
            updated_by=user.get("sub"),
            updated_at=datetime.utcnow().isoformat()
        )
        db.add(config)

    # Log de evento
    log = EventLog(
        timestamp=datetime.utcnow().isoformat(),
        event_type="CONFIG_CHANGE",
        intersection_id=intersection_id,
        user_id=user.get("sub"),
        details=f'{{"green_time": {green_time}, "red_time": {red_time}}}'
    )
    db.add(log)
    db.commit()

    return {
        "status": "updated",
        "intersection": intersection_id,
        "green_time": green_time,
        "red_time": red_time
    }


@router.post("/lights/{intersection_id}/fault")
def trigger_fault(
    intersection_id: str,
    db: Session = Depends(get_db),
    user=Depends(require_role("control"))
):
    """
    Simula un fallo manual en un semáforo específico (conmutación/toggle).
    El semáforo pasará a estado FAULT si está normal, o se recuperará si ya está en fallo.
    Requiere rol 'control'.
    """
    engine = get_engine()

    # Buscar intersección
    if intersection_id not in engine.network.nodes:
        raise HTTPException(status_code=404, detail="Intersección no encontrada")

    intersection = engine.network.nodes[intersection_id]
    
    # Conmutar estado de fallo del semáforo
    if intersection.light.state == "FAULT":
        intersection.light.restore()
        status = "fault_restored"
        event_type = "RESTORE"
    else:
        intersection.light.trigger_fault()
        status = "fault_triggered"
        event_type = "FAULT"

    # Registrar el evento en el log de auditoría
    log = EventLog(
        timestamp=datetime.utcnow().isoformat(),
        event_type=event_type,
        intersection_id=intersection_id,
        user_id=user.get("sub"),
        details=f'{{"source": "manual_control", "action": "{status}"}}'
    )
    db.add(log)
    db.commit()

    return {"status": status, "intersection": intersection_id}


@router.get("/lights")
def get_lights(db: Session = Depends(get_db), user=Depends(require_role("control"))):
    """
    Lista la configuración de todos los semáforos.
    Incluye tiempos actuales y última modificación.
    Requiere rol 'control'.
    """
    configs = db.query(LightConfig).all()
    return [
        {
            "intersection_id": c.intersection_id,
            "green_time": c.green_time,
            "red_time": c.red_time,
            "updated_by": c.updated_by,
            "updated_at": c.updated_at
        }
        for c in configs
    ]


@router.get("/logs")
def get_logs(
    event_type: str | None = None,
    limit: int = 100,
    db: Session = Depends(get_db),
    user=Depends(require_role("control"))
):
    """
    Obtiene los últimos eventos del log de eventos.
    Permite filtrar por tipo de evento y limitar resultados.
    Requiere rol 'control'.
    """
    query = db.query(EventLog)
    
    if event_type:
        query = query.filter(EventLog.event_type == event_type)
    
    logs = query.order_by(EventLog.timestamp.desc()).limit(limit).all()
    
    return [
        {
            "id": log.id,
            "timestamp": log.timestamp,
            "event_type": log.event_type,
            "intersection_id": log.intersection_id,
            "vehicle_id": log.vehicle_id,
            "details": log.details,
            "user_id": log.user_id
        }
        for log in logs
    ]
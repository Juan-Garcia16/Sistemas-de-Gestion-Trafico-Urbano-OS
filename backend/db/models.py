from sqlalchemy import Column, Integer, String, Text
from db.database import Base


class User(Base):
    """
    Modelo de Usuario para autenticación y autorización.
    Cada usuario tiene un rol que determina sus permisos en el sistema.
    """
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "viewer" (solo lectura) o "control" (modificación)


class EventLog(Base):
    """
    Log de eventos del sistema para auditoría y depuración.
    Registra fallos, emergencias, cambios de configuración y deadlocks.
    """
    __tablename__ = "event_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(String, nullable=False)
    event_type = Column(String, nullable=False)  # FAULT | EMERGENCY | CONFIG_CHANGE | DEADLOCK
    intersection_id = Column(String, nullable=True)
    vehicle_id = Column(String, nullable=True)
    details = Column(Text, nullable=True)  # JSON string con contexto adicional
    user_id = Column(String, nullable=True)  # Usuario que realizó la acción


class LightConfig(Base):
    """
    Configuración persistente de tiempos de semáforos por intersección.
    Permite ajustar green_time y red_time según necesidades de tráfico.
    """
    __tablename__ = "light_config"

    intersection_id = Column(String, primary_key=True)
    green_time = Column(Integer, default=10)
    red_time = Column(Integer, default=10)
    updated_by = Column(String, nullable=True)
    updated_at = Column(String, nullable=True)
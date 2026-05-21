import os
from pathlib import Path
from pydantic import BaseModel


class Settings(BaseModel):
    """
    Configuración global del sistema usando Pydantic para validación.
    Todos los settings pueden ser sobrescritos por variables de entorno.
    """
    # Rutas
    BASE_DIR: Path = Path(__file__).resolve().parent
    DB_PATH: str = str(BASE_DIR / "traffic.db")

    # JWT
    JWT_SECRET: str = "traffic-system-secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 8

    # Simulación
    SIMULATION_TICK_INTERVAL: float = 1.0
    FAULT_MIN_INTERVAL: int = 15
    FAULT_MAX_INTERVAL: int = 30
    FAULT_RECOVERY_TIME: int = 5

    # Semáforos
    TRAFFIC_LIGHT_DEFAULT_GREEN: int = 10
    TRAFFIC_LIGHT_DEFAULT_RED: int = 10
    TRAFFIC_LIGHT_YELLOW_DURATION: int = 3

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = False


# Instancia global de configuración
settings = Settings()

# Exportar constantes para uso directo
BASE_DIR = settings.BASE_DIR
DB_PATH = settings.DB_PATH
JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM
JWT_EXPIRATION_HOURS = settings.JWT_EXPIRATION_HOURS
SIMULATION_TICK_INTERVAL = settings.SIMULATION_TICK_INTERVAL
FAULT_MIN_INTERVAL = settings.FAULT_MIN_INTERVAL
FAULT_MAX_INTERVAL = settings.FAULT_MAX_INTERVAL
FAULT_RECOVERY_TIME = settings.FAULT_RECOVERY_TIME
TRAFFIC_LIGHT_DEFAULT_GREEN = settings.TRAFFIC_LIGHT_DEFAULT_GREEN
TRAFFIC_LIGHT_DEFAULT_RED = settings.TRAFFIC_LIGHT_DEFAULT_RED
TRAFFIC_LIGHT_YELLOW_DURATION = settings.TRAFFIC_LIGHT_YELLOW_DURATION
API_HOST = settings.API_HOST
API_PORT = settings.API_PORT
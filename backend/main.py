from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes_auth import router as auth_router
from api.routes_simulation import router as simulation_router
from api.routes_control import router as control_router
from api.websocket import router as websocket_router, manager
from db.database import engine, Base

# Importaciones de módulos core existentes para verificar que existen
from core.traffic_light import TrafficLight
from core.vehicle import Vehicle, Priority
from core.scheduler import TrafficScheduler
from core.intersection import Intersection
from simulation.engine import SimulationEngine
from simulation.network import IntersectionNetwork


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan handler para startup y shutdown de la aplicación.
    Crea las tablas de la base de datos al iniciar.
    """
    # Startup: crear tablas de la base de datos
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: cleanup si es necesario


app = FastAPI(
    title="Traffic System API",
    description="API REST y WebSocket para el Sistema de Gestión de Tráfico Urbano",
    version="1.0.0",
    lifespan=lifespan
)

# Configuración CORS para permitir conexiones del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar origins específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Incluir routers
app.include_router(auth_router)
app.include_router(simulation_router)
app.include_router(control_router)
app.include_router(websocket_router)


@app.get("/")
def root():
    """Endpoint raíz con estado del sistema."""
    return {"status": "running", "system": "Traffic Management"}


@app.get("/health")
def health_check():
    """Endpoint de salud para verificar que el servidor está activo."""
    return {"status": "healthy"}
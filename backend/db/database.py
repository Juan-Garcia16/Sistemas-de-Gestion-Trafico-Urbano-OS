from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DB_PATH

# Engine SQLite con check_same_thread=False para FastAPI (múltiples threads)
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})

# SessionLocal para crear sesiones de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarative para los modelos
Base = declarative_base()


def get_db():
    """
    Dependency de FastAPI para obtener una sesión de DB.
    Garantiza que la sesión se cierre después de cada request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
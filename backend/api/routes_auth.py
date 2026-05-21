import uuid
import bcrypt

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import User
from auth.jwt_handler import create_token


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica que el password plano coincida con el hash."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_password_hash(password: str) -> str:
    """Genera hash bcrypt del password."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


router = APIRouter(prefix="/auth", tags=["Authentication"])


class RegisterRequest(BaseModel):
    """Modelo para el body de /auth/register"""
    username: str
    password: str
    role: str


@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario en el sistema.
    - username: debe ser único
    - password: se hashea con bcrypt
    - role: "viewer" (solo lectura) o "control" (modificación)
    """
    username = request.username
    password = request.password
    role = request.role

    # Validar rol
    if role not in ["viewer", "control"]:
        raise HTTPException(status_code=400, detail="Rol inválido. Use 'viewer' o 'control'")

    # Verificar si el usuario ya existe
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    # Crear usuario con password hasheado
    user = User(
        id=str(uuid.uuid4()),
        username=username,
        password_hash=get_password_hash(password),
        role=role
    )
    db.add(user)
    db.commit()

    return {"message": "User created", "user_id": user.id}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login de usuario. Retorna JWT token si las credenciales son válidas.
    Usa OAuth2PasswordRequestForm para compatibilidad con el flujo estándar.
    """
    # Buscar usuario
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    # Verificar password
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    # Generar token
    token = create_token(user.id, user.role)

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role
    }
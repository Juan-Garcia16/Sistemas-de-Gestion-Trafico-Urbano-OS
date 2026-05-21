from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRATION_HOURS

# Scheme OAuth2 para extraer token del header Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_token(user_id: str, role: str) -> str:
    """
    Crea un token JWT con el user_id y role del usuario.
    El token expira en JWT_EXPIRATION_HOURS horas.
    """
    payload = {
        "sub": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    """
    Decodifica y valida un token JWT.
    Retorna el payload si es válido.
    Lanza JWTError si expira o es inválido.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError as e:
        raise JWTError(f"Token inválido o expirado: {e}")


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Dependencia FastAPI para obtener el usuario actual desde el token JWT.
    Se usa en rutas protegidas para acceder al usuario autenticado.
    """
    try:
        payload = decode_token(token)
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
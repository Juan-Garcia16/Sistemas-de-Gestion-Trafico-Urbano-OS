from fastapi import Depends, HTTPException
from jose import JWTError

from auth.jwt_handler import oauth2_scheme, decode_token

# Roles válidos en el sistema
ROLES = ["viewer", "control"]


def require_role(required_role: str):
    """
    Decorador/dependencia FastAPI para proteger rutas por rol específico.
    Verifica que el usuario tenga el rol requerido.
    Retorna 403 si el rol es insuficiente, 401 si el token es inválido.
    """
    def dependency(token: str = Depends(oauth2_scheme)):
        try:
            payload = decode_token(token)
            if payload.get("role") != required_role:
                raise HTTPException(status_code=403, detail="Rol insuficiente")
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Token inválido")
    return dependency


def require_any_role(*roles):
    """
    Dependencia FastAPI alternativa que acepta cualquiera de los roles dados.
    Útil cuando múltiples roles pueden acceder a una ruta.
    """
    def dependency(token: str = Depends(oauth2_scheme)):
        try:
            payload = decode_token(token)
            user_role = payload.get("role")
            if user_role not in roles:
                raise HTTPException(status_code=403, detail="Rol insuficiente")
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Token inválido")
    return dependency


def get_optional_user():
    """
    Dependencia que retorna el usuario sin requerir autenticación.
    Retorna None si no hay token o el token es inválido.
    """
    def dependency(token: str = Depends(oauth2_scheme)):
        try:
            payload = decode_token(token)
            return payload
        except (JWTError, Exception):
            return None
    return dependency
from fastapi import WebSocket, WebSocketDisconnect
import json

from auth.jwt_handler import decode_token


class ConnectionManager:
    """
    Gestor de conexiones WebSocket para broadcast en tiempo real.
    Mantiene registro de todos los clientes conectados y permite
    enviar mensajes a todos ellos simultáneamente.
    """
    def __init__(self):
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        """Acepta y registra una nueva conexión WebSocket."""
        await ws.accept()
        self.active.append(ws)

    async def disconnect(self, ws: WebSocket):
        """Remueve una conexión del registro activo."""
        if ws in self.active:
            self.active.remove(ws)

    async def broadcast(self, data: dict):
        """
        Envía un mensaje JSON a todos los clientes conectados.
        Desconecta automáticamente clientes que ya no respondan.
        """
        msg = json.dumps(data)
        disconnected = []
        for ws in self.active:
            try:
                await ws.send_text(msg)
            except Exception:
                disconnected.append(ws)
        # Limpiar conexiones rotas
        for ws in disconnected:
            await self.disconnect(ws)

    async def send_personal(self, ws: WebSocket, data: dict):
        """Envía un mensaje a un cliente específico."""
        try:
            await ws.send_text(json.dumps(data))
        except Exception:
            await self.disconnect(ws)


# Instancia global del manager
manager = ConnectionManager()

# Router WebSocket
from fastapi import APIRouter

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    """
    Endpoint WebSocket para conexión en tiempo real.
    Recibe mensajes del cliente y mantiene la conexión activa.
    Los mensajes de estado se envían automáticamente desde el engine.
    """
    await manager.connect(ws)
    try:
        while True:
            # Receive messages from client (keep-alive, ping, etc)
            data = await ws.receive_text()
            # Echo back para mantener alive (opcional)
            try:
                await ws.send_text(json.dumps({"type": "PONG", "data": data}))
            except Exception:
                await manager.disconnect(ws)
                break
    except WebSocketDisconnect:
        await manager.disconnect(ws)
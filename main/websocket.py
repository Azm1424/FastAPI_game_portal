from imports import APIRouter, WebSocket, WebSocketDisconnect, Dict, List, SECRET_KEY
import jwt


router = APIRouter()

class ConnectionManager:

    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.chat_history: Dict[str, List] = {}

    async def connect(self, websocket: WebSocket, game_id: str):
        try:
            await websocket.accept()
            if game_id not in self.active_connections:
                self.active_connections[game_id] = []
                self.chat_history[game_id] = []
            self.active_connections[game_id].append(websocket)
        except Exception as e:
            return {'mess': e}

    def disconnect(self, websocket: WebSocket, game_id: str):
        try:
            if game_id in self.active_connections:
                self.active_connections[game_id].remove(websocket)
                if not self.active_connections[game_id]:
                    del self.active_connections[game_id]
        except Exception as e:
            return {'mess': e}

    async def broadcast(self, message: str, game_id: str):
        try:
            if game_id in self.active_connections:
                for connection in self.active_connections[game_id]:
                    await connection.send_text(message)
                self.chat_history[game_id].append(message)
                if len(self.chat_history[game_id]) > 100:
                    self.chat_history[game_id].pop(0)
        except Exception as e:
            return {'mess': e}

@router.websocket("/ws/game/{id}")
async def websocket_endpoint(websocket: WebSocket, id: str):
    from main import manager
    await manager.connect(websocket, id)
    token = websocket.cookies.get('access_token')
    username = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])['sub']
    try:
        while True:
            data = await websocket.receive_text()
            if data:
                await manager.broadcast(f"{username}: {data}", id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, id)
    except Exception as e:
        print(f"Error: {e}")
        manager.disconnect(websocket, id)
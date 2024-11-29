from fastapi import WebSocket, WebSocketDisconnect

class WebSocketManager:
    def __init__(self):
        self.active_connections = set()
        self.commands = ''

    def add_command(self, command):
        self.commands += command

    async def connect(self, websocket: WebSocket):
        """Accept and register a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.add(websocket)
        print("Client established connection")

    async def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        self.active_connections.remove(websocket)
        print("Client disconnected")

    async def send(self):
        """Send a message to all active WebSocket connections."""
        for connection in self.active_connections:
            await connection.send_text(self.commands)

    async def receive_message(self, websocket: WebSocket):
        """Wait for and process messages from the WebSocket connection."""
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            await self.disconnect(websocket)

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
from .cardholder import Cardholder
from .device import Device
import json
app = FastAPI()

active_connections = set()


@app.get('/{device_id}/{card_id}')
async def process_card(card_id: str, device_id: int) -> str:
    try:
        device = Device(device_id)
        cardholder = Cardholder(card_id)
        device.register(cardholder)
        if cardholder.role == 'teacher':
            for connection in active_connections:
                await connection.send_text(device.websocket_commands)
            
        return device.message
    except Exception as e:
        print(str(e))
        return "刷卡失敗"


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    print("Client established connection")
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(websocket)

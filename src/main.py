from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
from .cardholder import Cardholder
from .device import Device
import base64
import requests
import json
app = FastAPI()

active_connections = set()


@app.get('/{device_id}/{card_id}')
async def process_card(card_id: str, device_id: int) -> str:
    try:
        device = Device(device_id)  # Initialize Device
        cardholder = Cardholder(card_id)  # Initialize Cardholder
        output = device.register(cardholder)
        if cardholder.identity == 'teacher':
            #    image_url = "https://via.placeholder.com/150"
            #    response = requests.get(image_url)
            #    response.raise_for_status()
            #    base64_string = base64.b64encode(response.content).decode("utf-8")
            #    message = {
            #     "name": "example",  # Example name for the image
            #     "image": base64_string
            # }
            for connection in active_connections:
                await connection.send_text(json.dumps({
                    "id": device.id,
                    "name": cardholder.name,
                    "school": cardholder.school if not None else "",
                }))
        return output  # Return the output from register
    except Exception as e:
        print(str(e))
        return "刷卡失敗"


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(websocket)

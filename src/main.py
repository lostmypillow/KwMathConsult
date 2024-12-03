from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from .cardholder import Cardholder
from .device import Device
from typing import Optional

app = FastAPI()

active_websocket: Optional[WebSocket] = None

@app.get('/{device_id}/{card_id}')
async def process_card(card_id: str, device_id: int) -> str:
    try:
        device = Device(device_id)
        await device.register(Cardholder(card_id), active_websocket)
        return device.message
    except Exception as e:
        print(str(e))
        return "刷卡失敗"


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global active_websocket
    await websocket.accept()
    active_websocket = websocket
    print("client connected")
    for n in range(1, 7):
        device = Device(n)
        print(device.teacher_id)
        if device.teacher_id is not None:
            teacher = Cardholder(device.teacher_id)
            await websocket.send_json(
                {
                    "device": device.id,
                    "image": teacher.id,
                    "teacher": teacher.name,
                    "school": teacher.school
                }
            )
    try:
        while True:

            message = await websocket.receive_text()

    except WebSocketDisconnect:
        active_websocket = None
        print("Client disconnected")

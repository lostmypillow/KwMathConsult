from fastapi import FastAPI, WebSocket
from .cardholder import Cardholder
from .device import Device
from .websocket_manager import WebSocketManager
app = FastAPI()

websocket_manager = WebSocketManager()


@app.get('/{device_id}/{card_id}')
async def process_card(card_id: str, device_id: int) -> str:
    try:
        device = Device(device_id, websocket_manager) 
        device.register(Cardholder(card_id))
        return device.message
    except Exception as e:
        print(str(e))
        return "刷卡失敗"


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    for n in range(1, 7):
        device = Device(n)
        if device.teacher_id is not None:
            teacher = Cardholder(device.teacher_id)
            websocket_manager.add_command(f'ADD {device.id} {teacher.id} {teacher.name} {teacher.school};')
            websocket_manager.send()

    await websocket_manager.receive_message(websocket)

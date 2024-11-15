from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
from .cardholder import Cardholder
from .device import Device
app = FastAPI()

connected_clients: List[WebSocket] = []


@app.get('/{device_id}/{card_id}')
def process_card(card_id: str, device_id: int) -> str:
    try:
        device = Device(device_id)  # Initialize Device
        cardholder = Cardholder(card_id)  # Initialize Cardholder
        output = device.register(cardholder)
        for_websocket = output.replace("老師", "").replace("學生", "")
        # for-websocket must have "device_num-teacher_name-teacher_school-teacher_img_url"
        # Call register method
        message = {
            "number": 1,
            "teacher_name": "王小名",
            "teacher_school": "建國中學",
            "teacher_img": "./test.jpg",
        },
        return output  # Return the output from register
    except Exception as e:
        print(str(e))
        return "刷卡失敗"  # Handle exceptions


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            # Keep connection open and await messages
            data = await websocket.receive_text()
            await websocket.send_text(f"Received: {data}")
    except WebSocketDisconnect:
        connected_clients.remove(websocket)


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}

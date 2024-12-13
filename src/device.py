from .database import execute_SQL
from .cardholder import Cardholder
from fastapi import WebSocket


class Device:
    def __init__(self, device_id):
        self.teacher_id = None
        self.id = device_id
        self.message = ""
        self._check_db_exists()
        self._check_for_teacher()
        

    def _check_for_teacher(self):
        result = execute_SQL(
            "check_for_teacher",
            device_id=self.id
        )
        if result and result.老師編號 is not None:
            self.teacher_id = result.老師編號
    def _check_db_exists(self):
        execute_SQL("check_device_db")

    async def register(self, cardholder: Cardholder, websocket: WebSocket):
        if cardholder.is_student and self.teacher_id == None:
            self.message = '刷卡失敗: 輔導老師未刷卡'
        elif cardholder.is_student and self.teacher_id is not None:
            reservation_id = execute_SQL(
                "register_select",
                student_id=cardholder.id,
                teacher_id=self.teacher_id
            )

            if not reservation_id or reservation_id == None:
                execute_SQL(
                    "register_insert",
                    student_id=cardholder.id,
                    teacher_id=self.teacher_id
                )
                self.message = f'{cardholder.name}學生 刷卡成功'

            else:
                execute_SQL(
                    "register_update_student",
                    reservation_id=reservation_id.自動編號
                )
                self.message = f'{cardholder.name}學生 刷卡成功'

        elif cardholder.is_teacher:
            # Check if the cardholder's device is this device (self.id)
            if cardholder.device_id == self.id:
                print('same')
                # If the device matches, clear this device and stop further processing
                execute_SQL(
                    "register_update_teacher",
                    teacher_id=None,
                    device_id=self.id
                )
                if websocket is not None:
                    await websocket.send_json({
                        "device": self.id,
                        "image": "",
                        "teacher": "",
                        "school": ""
                    })
                self.message = f'{cardholder.name}老師 刷卡成功'
                return

            # If cardholder has a device assigned and it's not this device
            elif cardholder.device_id is not None and cardholder.device_id != self.id:
                print("swap")
                # Clear the cardholder's device (not the current one)
                execute_SQL(
                    "register_update_teacher",
                    teacher_id=None,
                    device_id=cardholder.device_id
                )
                if websocket is not None:
                    await websocket.send_json({
                        "device": cardholder.device_id,
                        "image": "",
                        "teacher": "",
                        "school": ""
                    }
                    )

            # Finally, assign this device to the cardholder
            execute_SQL(
                "register_update_teacher",
                teacher_id=cardholder.id,
                device_id=self.id
            )
            if websocket is not None:
                await websocket.send_json(
                    {
                        "device": self.id,
                        "image": cardholder.id,
                        "teacher": cardholder.name,
                        "school": cardholder.school
                    }
                )
            self.message = f'{cardholder.name}老師 刷卡成功'
        else:
            self.message = '刷卡失敗: 查無此號'

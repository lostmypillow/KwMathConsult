from .database import Database
from .cardholder import Cardholder
from fastapi import WebSocket
class Device:
    def __init__(self, device_id):
        self.teacher_id = None
        self.id = device_id
        self.message = ""
        self._check_for_teacher()

    def _check_for_teacher(self):
        result = Database.execute_SQL(
            "_check_for_teacher", {'device_id': self.id})
        self.teacher_id = result.老師編號 if result and result.老師編號 is not None else None

    async def register(self, cardholder: Cardholder, websocket: WebSocket):
        if cardholder.is_student and self.teacher_id == None:
            self.message = '刷卡失敗: 輔導老師未刷卡'
        elif cardholder.is_student and self.teacher_id is not None:
            reservation_id = Database.execute_SQL(
                "register_select", {'student_id': cardholder.id, 'teacher_id': self.teacher_id})

            if not reservation_id or reservation_id == None:
                Database.execute_SQL("register_insert", {
                                     'student_id': cardholder.id, 'teacher_id': self.teacher_id})
                self.message = f'{cardholder.name}學生 刷卡成功'

            else:
                Database.execute_SQL("register_update_student", {
                                     'reservation_id': reservation_id.自動編號})
                self.message = f'{cardholder.name}學生 刷卡成功'

        elif cardholder.is_teacher:
            def params_lambda(teacher_id, device_id): return {
                'teacher_id': teacher_id, 'device_id': device_id}
            # Check if the cardholder's device is this device (self.id)
            if cardholder.device_id == self.id:
                print('same')
                # If the device matches, clear this device and stop further processing
                Database.execute_SQL(
                    "register_update_teacher", params_lambda(None, self.id))
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
                Database.execute_SQL("register_update_teacher", params_lambda(
                    None, cardholder.device_id))
                await websocket.send_json({
                    "device": cardholder.device_id,
                    "image": "",
                    "teacher": "",
                    "school": ""
                })


            # Finally, assign this device to the cardholder
            Database.execute_SQL("register_update_teacher",
                                 params_lambda(cardholder.id, self.id))
            await websocket.send_json(
                {
                    "device": self.id,
                    "image": cardholder.id,
                    "teacher": cardholder.name,
                    "school": cardholder.school
                })
            self.message = f'{cardholder.name}老師 刷卡成功'
        else:
            self.message = '刷卡失敗: 查無此號'

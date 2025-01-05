from .database_handler import DatabaseHandler
from .cardholder_service import CardholderService as Cardholder
class DeviceService:
    def __init__(self, device_id):
        self.device_id = device_id
        self.teacher_id = None
        self.message = ""
    def _initialize_device(self):
        self._assign_teacher_if_exists()
    def _assign_teacher_if_exists(self):
        result = DatabaseHandler.check_for_teacher(self.device_id)
        self.teacher_id = result.老師編號 if result and result.老師編號 is not None else ""
    def handle_registration(self, cardholder: Cardholder):
        """Handles the registration process for both students and teachers."""
        if cardholder.is_student:
            return self._register_student(cardholder)
        elif cardholder.is_teacher:
            return self._register_teacher(cardholder)
        else:
            self.message = '刷卡失敗: 查無此號'
            return self.message
    def _register_student(self, cardholder: Cardholder):
        """Handles student registration logic."""
        if self.teacher_id is None:
            self.message = '刷卡失敗: 輔導老師未刷卡'
            return self.message
        reservation_id = DatabaseHandler.register_student(cardholder.id, self.teacher_id)
        if not reservation_id:
            DatabaseHandler.insert_student_registration(cardholder.id, self.teacher_id)
            self.message = f'{cardholder.name}學生 刷卡成功'
        else:
            DatabaseHandler.update_student_registration(reservation_id.自動編號)
            self.message = f'{cardholder.name}學生 刷卡成功'
        return self.message

    def _register_teacher(self, cardholder: Cardholder):
        """Handles teacher registration logic."""
        if cardholder.device_id == self.device_id:
            return self._clear_teacher_from_device(cardholder)
        else:
            return self._swap_teacher_device(cardholder)

    def _clear_teacher_from_device(self, cardholder: Cardholder):
        """Clears the teacher from the device."""
        DatabaseHandler.update_teacher_registration(None, self.device_id)
        self.message = f'{cardholder.name}老師 刷卡成功'
        return self.message

    def _swap_teacher_device(self, cardholder: Cardholder):
        """Swaps the teacher from one device to another."""
        if cardholder.device_id:
            DatabaseHandler.update_teacher_registration(None, cardholder.device_id)
        DatabaseHandler.update_teacher_registration(cardholder.id, self.device_id)
        self.message = f'{cardholder.name}老師 刷卡成功'
        return self.message
from .database import Database
from .cardholder import Cardholder


class Device:
    """
    A class representing a device used by either a teacher or a student. 
    The device can register a cardholder (either a student or a teacher) 
    based on the current state of the device's registration.
    """

    def __init__(self, device_id):
        """
        Initializes a Device instance.

        Args:
            device_id (str): The unique identifier for the device.
        """
        self.teacher_id = None
        """The ID of the teacher assigned to the device, if any."""
        self.id = device_id
        """The unique identifier for the device."""
        self._check_for_teacher()

    def _check_for_teacher(self):
        """
        Checks if the device is associated with a teacher by querying the database.
        Sets the teacher_id attribute if a teacher is found.

        This method uses the Database class to query the device's teacher assignment.
        """
        result = Database.execute_SQL(
            "_check_for_teacher", {'device_id': self.id})
        self.teacher_id = result.老師編號 if result and result.老師編號 is not None else None

    def register(self, cardholder: Cardholder):
        """
        Registers a student or teacher to the device.

        Args:
            cardholder (Cardholder): from `classes.cardholder.Cardholder`

        Returns:
            dict: A dictionary with a message indicating the result of the registration attempt.

        The behavior depends on the type of cardholder:
        - For students: If no teacher is associated with the device, registration fails. 
        If a teacher is assigned, a reservation is created or updated.
        - For teachers: If the teacher already has a device assigned, the previous device is cleared, and this device is assigned.
        """
        if cardholder.is_student and self.teacher_id == None:
            return {'message': '刷卡失敗: 輔導老師未刷卡'}
        elif cardholder.is_student and self.teacher_id is not None:
            reservation_id = Database.execute_SQL(
                "register_select", {'student_id': cardholder.id, 'teacher_id': self.teacher_id})

            if not reservation_id or reservation_id == None:
                Database.execute_SQL("register_insert", {
                                     'student_id': cardholder.id, 'teacher_id': self.teacher_id})
                return {'message': f'{cardholder.name}學生 刷卡成功'}
            else:
                Database.execute_SQL("register_update_student", {
                                     'reservation_id': reservation_id.自動編號})
                return {'message': f'{cardholder.name}學生 刷卡成功'}
        elif cardholder.is_teacher:
            def params_lambda(teacher_id, device_id): return {
                'teacher_id': teacher_id, 'device_id': device_id}
            # Check if the cardholder's device is this device (self.id)
            if cardholder.device_id == self.id:
                # If the device matches, clear this device and stop further processing
                Database.execute_SQL(
                    "register_update_teacher", params_lambda(None, self.id))
                return {'message': f'{cardholder.name}老師 刷卡成功'}

            # If cardholder has a device assigned and it's not this device
            if cardholder.device_id is not None:
                # Clear the cardholder's device (not the current one)
                Database.execute_SQL("register_update_teacher", params_lambda(
                    None, cardholder.device_id))

            # Finally, assign this device to the cardholder
            Database.execute_SQL("register_update_teacher",
                                 params_lambda(cardholder.id, self.id))
            return {'message': f'{cardholder.name}老師 刷卡成功'}

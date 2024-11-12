from .database import Database
from .cardholder import Cardholder


class Device:
    def __init__(self, device_id):
        self.teacher_id = None
        self.id = device_id
        self.check_for_teacher()

    def _check_for_teacher_(self):
        query = "SELECT 老師編號 FROM dbo.設備資料 WHERE 設備號碼 = :device_id"
        result = Database.execute_query(query, {'device_id': self.id})
        self.teacher_id = result.老師編號 if result and result.老師編號 is not None else None

    def register(self, cardholder: Cardholder):

        if cardholder.is_student:
            reservation_query = """
            SELECT 自動編號
            FROM dbo.預約輔導
            WHERE 日期 = convert(varchar, getdate(), 111)
            AND 學號 = :student_id
            AND 老師編號 = :teacher_id
            AND 下課時間 IS NULL
            """
            insert_query = """
            INSERT INTO dbo.預約輔導 (日期, 學號, 老師編號, 上課時間)
            VALUES (convert(varchar, getdate(), 111), :student_id, :teacher_id, GETDATE())
            """
            update_query = """
            UPDATE dbo.預約輔導
            SET 下課時間 = GETDATE()
            WHERE 自動編號 = :reservation_id
            """
            reservation_id = Database.execute_query(reservation_query, {'student_id': student_id, 'teacher_id': teacher_id})
            if not reservation_id:
            conn.execute(text(insert_query), {
                         'student_id': student_id, 'teacher_id': teacher_id})
            conn.commit()
        else:
            conn.execute(text(update_query), {
                         'reservation_id': reservation_id.自動編號})
            conn.commit()
        elif cardholder.is_teacher:
            SQL_update = "UPDATE dbo.設備資料 SET 老師編號 = :teacher_id WHERE 設備號碼 = :device_id"
            params_lambda = lambda teacher_id, device_id : {'teacher_id': teacher_id, 'device_id': device_id}
            # Check if the cardholder's device is this device (self.id)
            if cardholder.device_id == self.id:
            # If the device matches, clear this device and stop further processing
                Database.execute_update(SQL_update, params_lambda(None, self.id))
                return  # Exit early as we don't need to do any further updates

            # If cardholder has a device assigned and it's not this device
            if cardholder.device_id is not None:
                # Clear the cardholder's device (not the current one)
                Database.execute_update(SQL_update, params_lambda(None, cardholder.device_id))

            # Finally, assign this device to the cardholder
            Database.execute_update(SQL_update, params_lambda(cardholder.id, self.id))

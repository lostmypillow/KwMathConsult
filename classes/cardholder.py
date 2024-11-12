from .database import Database


class Cardholder:
    def __init__(self, card_id):
        self.params = {'card_id': self.card_id}
        self.identity = None
        self.id = None
        self.name = None
        self.device_id = None
        self.fetch_identity()
        self._fetch_associated_device()

    def _fetch_identity(self):
        student_query = "SELECT 姓名, 學號 FROM dbo.學生資料 WHERE 卡號 = :card_id or 學號 = :card_id"
        teacher_query = "SELECT 姓名, 學號 FROM dbo.使用者 WHERE 卡號 = :card_id or 學號 = :card_id"
        student = Database.execute_query(student_query, self.params)
        if student:
            self.identity = "student"
            self.name = student.姓名
            self.id = student.學號
        else:
            teacher = Database.execute_query(teacher_query, self.params)
            if teacher:
                self.identity = "teacher"
                self.name = teacher.姓名
                self.id = teacher.學號

    def _fetch_associated_device(self) -> bool:
        select_query = "SELECT 設備號碼 FROM dbo.設備資料 WHERE 老師編號 = :teacher_id"
        if self.id is not None:
            device_result = Database.execute_query(select_query, {'teacher_id': self.id})
            if device_result and device_result.設備號碼 is not None:
                self.device_id = device_result.設備號碼


    @property
    def is_student(self) -> bool:
        """Return True if the cardholder is a student."""
        return self.identity == "student"

    @property
    def is_teacher(self) -> bool:
        """Return True if the cardholder is a teacher."""
        return self.identity == "teacher"
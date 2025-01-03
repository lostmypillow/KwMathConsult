from .database import execute_SQL
from .database_handler import DatabaseHandler


class CardholderService:
    """
    A class representing a cardholder (either a student or a teacher) with associated information such as role, ID, name, and device.
    """

    def __init__(self, card_id):
        """
        Initializes a CardholderService instance and attempts to fetch the cardholder's role and associated device (if applicable).
        """
        self.role = None
        """Can be either 'student' or 'teacher'."""
        self.id = None
        """學號"""
        self.name = None
        self.school = None
        self.device_id = None
        self.status = ""
        """Number of the device that this teacher has already scanned."""
        self._fetch_role(card_id)
        """Fetches role upon instantiation."""

    def _fetch_role(self, card_id):
        student = DatabaseHandler.fetch_student_role(card_id)
        print(student)
        if student:
            self.role = "student"
            self.name = student.姓名.strip()
            self.id = student.學號.strip()
        else:
            teacher = DatabaseHandler.fetch_teacher_role(card_id)
            if teacher:
                self.role = "teacher"
                self.name = teacher.姓名.strip()
                self.id = teacher.學號.strip()
                self.school = teacher.大學.strip()
                self.device_id = self._fetch_device_for_teacher(teacher.學號)
            else:
                self.role = "other"
                self.name = "Not Found"
                self.id = "Not Found"

    def _fetch_device_for_teacher(self, teacher_id):
        """
        Fetches the associated device for a teacher.
        """
        device_data = DatabaseHandler.fetch_associated_device(teacher_id)
        return device_data.設備號碼 if device_data and device_data.設備號碼 else None

    @property
    def is_student(self) -> bool:
        return self.role == "student"

    @property
    def is_teacher(self) -> bool:
        return self.role == "teacher"

from .database import Database


class Cardholder:
    """
    A class representing a cardholder (either a student or a teacher) with associated information such as role, ID, name, and device.
    """

    def __init__(self, card_id):
        """
        Initializes a Cardholder instance and attempts to fetch the cardholder's role and associated device (if applicable).
        """
        self.role = None
        """Can be either 'student' or 'teacher'."""
        self.id = None
        """學號"""
        self.name = None
        self.school = None
        self.device_id = None
        self.status = ""
        print("im here")
        """Number of the device that this teacher has already scanned."""
        self._fetch_role(card_id)
        """Fetches role upon instantiation."""

    def _fetch_role(self, card_id):
        student = Database.execute_SQL("fetch_role_student", {
                                       'card_id': card_id})
        if student:
            self.role = "student"
            self.name = student.姓名.strip()
            self.id = student.學號.strip()
        else:
            teacher = Database.execute_SQL(
                "fetch_role_teacher", {'card_id': card_id})
            if teacher:

                self.role = "teacher"
                self.name = teacher.姓名.strip()
                self.id = teacher.學號.strip()
                self.school = teacher.大學.strip()

                device_result = Database.execute_SQL(
                    "_fetch_associated_device", {'teacher_id': teacher.學號})
                self.device_id = device_result.設備號碼 if device_result and device_result.設備號碼 is not None else None
            else:
                self.role = "other"
                self.name = "Not Found"
                self.id = "Not Found"

    @property
    def is_student(self) -> bool:
        return self.role == "student"

    @property
    def is_teacher(self) -> bool:
        return self.role == "teacher"

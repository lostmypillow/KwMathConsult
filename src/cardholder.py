from .database import Database


class Cardholder:
    """
    A class representing a cardholder (either a student or a teacher) with associated information such as identity, ID, name, and device.
    """

    def __init__(self, card_id):
        """
        Initializes a Cardholder instance and attempts to fetch the cardholder's identity and associated device (if applicable).
        """
        self.card_id = card_id
        """Can be either 卡號 or 學號. Used in private function `_fetch_identity`. Not to be confused with `Cardholder.id`."""
        self.identity = None
        """Can be either 'student' or 'teacher'."""
        self.id = None
        """學號 of card holder."""
        self.name = None
        """Name of card holder."""
        self.school = None
        self.device_id = None
        """Number of the device that this teacher has already scanned."""
        self._fetch_identity()
        """Fetches identity upon instantiation."""
        self._fetch_associated_device()
        """Fetches device number associated with the teacher if applicable."""

    def _fetch_identity(self):
        """
        Tries to determine the cardholder's identity (student or teacher) by querying the database.

        This private method first checks if the cardholder is a student by querying the database. 
        If no student record is found, it attempts to find a teacher record. It updates the 
        `identity`, `name`, and `id` attributes accordingly.

        This function will update:
            - `identity` to either "student" or "teacher".
            - `name` to the name of the student or teacher.
            - `id` to the corresponding student or teacher ID.
        """
        student = Database.execute_SQL("fetch_identity_student", {
                                       'card_id': self.card_id})
        if student:
            self.identity = "student"
            self.name = student.姓名
            self.id = student.學號
        else:
            teacher = Database.execute_SQL("fetch_identity_teacher", {
                                           'card_id': self.card_id})
            if teacher:
                self.identity = "teacher"
                self.name = teacher.姓名
                self.id = teacher.學號
                self.school = teacher.大學
            else:
                self.identity = "other"
                self.name = "Not Found"
                self.id = "Not Found"

    def _fetch_associated_device(self) -> bool:
        """
        Fetches the device number associated with the cardholder, if the cardholder is a teacher.

        This method will only fetch the associated device if the cardholder is identified as a teacher 
        and if a device is associated with their ID in the database.

        Returns:
            bool: True if the device number is successfully fetched, False otherwise.
        """
        if self.id is not None and self.identity == "teacher":
            device_result = Database.execute_SQL(
                "_fetch_associated_device", {'teacher_id': self.id})
            if device_result and device_result.設備號碼 is not None:
                self.device_id = device_result.設備號碼
                return True
        return False

    @property
    def is_student(self) -> bool:
        """
        Returns whether the cardholder is a student.

        Returns:
            bool: True if the cardholder's identity is "student", False otherwise.
        """
        return self.identity == "student"

    @property
    def is_teacher(self) -> bool:
        """
        Returns whether the cardholder is a teacher.

        Returns:
            bool: True if the cardholder's identity is "teacher", False otherwise.
        """
        return self.identity == "teacher"

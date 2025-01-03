from sqlalchemy import create_engine, text
import os

# Connection URL
connection_url = "mssql+pyodbc://testsql:test123456@192.168.2.8/JLL2?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes" 

# if os.getenv('DEBUG') == 'True' else "mssql+pyodbc://mssql:mssql@192.168.2.12/JLL2?driver=ODBC+Driver+17+for+SQL+Server"

# Engine
engine = create_engine(connection_url)

class DatabaseHandler:
    @staticmethod
    def execute_sql(command_name: str, mode: str = 'one', **kwargs):
        """Executes SQL commands synchronously."""
        file_path = './sql/' + command_name + '.sql'
        with open(file_path, 'r', encoding="utf-8") as file_buffer:
            sql_statement = file_buffer.read()

        with engine.connect() as conn:
            result = conn.execute(text(sql_statement), kwargs)
            if command_name in [
                "register_insert",
                "register_update_student", "register_update_teacher", "check_device_db"
            ]:
                conn.commit()
            else:
                return result.fetchone()
    @staticmethod
    def check_device_table():
        """Check if the device table exists in the database."""
        return DatabaseHandler.execute_sql("check_device_db")

    @staticmethod
    def check_for_teacher(device_id):
        """Check if a teacher is assigned to the given device."""
        return DatabaseHandler.execute_sql(
            "check_for_teacher", device_id=device_id
        )
    
    @staticmethod
    def register_student(student_id, teacher_id):
        """Registers a student with the teacher."""
        return DatabaseHandler.execute_sql(
            "register_select", student_id=student_id, teacher_id=teacher_id
        )

    @staticmethod
    def insert_student_registration(student_id, teacher_id):
        """Inserts a student reservation."""
        DatabaseHandler.execute_sql(
            "register_insert", student_id=student_id, teacher_id=teacher_id
        )

    @staticmethod
    def update_student_registration(reservation_id):
        """Updates an existing student registration."""
        DatabaseHandler.execute_sql(
            "register_update_student", reservation_id=reservation_id
        )

    @staticmethod
    def update_teacher_registration(teacher_id, device_id):
        """Updates the teacher assigned to a device."""
        DatabaseHandler.execute_sql(
            "register_update_teacher", teacher_id=teacher_id, device_id=device_id
        )
    @staticmethod
    def fetch_student_role(card_id):
        DatabaseHandler.execute_sql(
            "fetch_role_student",
            card_id=card_id
        )
    @staticmethod
    def fetch_teacher_role(card_id):
        DatabaseHandler.execute_sql(
                "fetch_role_teacher",
                card_id=card_id
            )
    @staticmethod
    def fetch_associated_device(teacher_id):
        """Fetches the associated device for a teacher."""
        DatabaseHandler.execute_sql("fetch_associated_device", teacher_id=teacher_id)

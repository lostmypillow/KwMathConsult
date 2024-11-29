from sqlalchemy import create_engine, text
import os

engine = create_engine(
    f"mssql+pyodbc://{os.environ.get('DB_USERNAME')}:"
    f"{os.environ.get('DB_PASSWORD')}@"
    f"{os.environ.get('DB_HOST')}/"
    f"{os.environ.get('DB_NAME')}?driver=ODBC+Driver+17+for+SQL+Server"
)
"""Engine creation using SQLAlchemy"""


class Database:
    """
    A class to interact with the database, executing SQL queries for various operations related to cardholders, devices, and reservations.
    """

    SQL_commands = {
        "fetch_role_student": f"""
            SELECT 姓名, 學號
            FROM {os.environ.get('STUDENT_DB_NAME')}
            WHERE 卡號 = :card_id OR 學號 = :card_id
        """,
        # 大學 might change
        "fetch_role_teacher": f"""
            SELECT 姓名, 學號, 大學
            FROM {os.environ.get('TEACHER_DB_NAME')}
            WHERE 卡號 = :card_id OR 學號 = :card_id""",
        "_fetch_associated_device": f"""
            SELECT 設備號碼
            FROM {os.environ.get('DEVICE_DB_NAME')}
            WHERE 老師編號 = :teacher_id
        """,
        "_check_for_teacher": f"""
            SELECT 老師編號
            FROM {os.environ.get('DEVICE_DB_NAME')}
            WHERE 設備號碼 = :device_id
        """,
        "register_select": f"""
            SELECT 自動編號
            FROM {os.environ.get('RESERVATION_DB_NAME')}
            WHERE 日期 = convert(varchar, getdate(), 111)
            AND 學號 = :student_id
            AND 老師編號 = :teacher_id
            AND 下課時間 IS NULL
        """,
        "register_insert": f"""
            INSERT INTO {os.environ.get('RESERVATION_DB_NAME')} (日期, 學號, 老師編號, 上課時間)
            VALUES (convert(varchar, getdate(), 111), :student_id, :teacher_id, GETDATE())
        """,
        "register_update_student": f"""
            UPDATE {os.environ.get('RESERVATION_DB_NAME')}
            SET 下課時間 = GETDATE()
            WHERE 自動編號 = :reservation_id
        """,
        "register_update_teacher": f"""
            UPDATE {os.environ.get('DEVICE_DB_NAME')}
            SET 老師編號 = :teacher_id
            WHERE 設備號碼 = :device_id
        """,
    }
    """A dictionary containing SQL queries associated with different database operations."""

    @staticmethod
    def execute_SQL(query_key: str, params: dict = None):
        """
        Executes a SQL query based on the provided query key and parameters.
        """
        query = Database.SQL_commands.get(query_key)
        with engine.connect() as conn:
            # For queries that modify data (insert, update), execute and commit the changes
            if query_key in ["register_insert", "register_update_student", "register_update_teacher"]:
                conn.execute(text(query), params)
                conn.commit()
            else:
                # For select queries, execute and return the first row of the result
                result = conn.execute(text(query), params)
                return result.fetchone()

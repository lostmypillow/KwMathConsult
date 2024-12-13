from sqlalchemy import create_engine, text
import os

# I'm using ODBC Driver 17, and I *could* use 18 and that would mean appending '&TrustServerCertificate=yes' at the end and testing extensively to ensure no broken functionality.
# So maybe after everything is stable and open a PR or something

engine = create_engine(
    f"mssql+pyodbc://{os.environ.get('DB_USERNAME')}:"
    f"{os.environ.get('DB_PASSWORD')}@"
    f"{os.environ.get('DB_HOST')}/"
    f"{os.environ.get('DB_NAME')}?driver=ODBC+Driver+17+for+SQL+Server"
)
"""Engine creation using SQLAlchemy"""


def execute_SQL(command_name: str, mode: str = 'one', **kwargs):

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
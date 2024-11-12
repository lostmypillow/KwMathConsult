from sqlalchemy import create_engine, text
import os

engine = create_engine(
    f'mssql+pyodbc://{os.environ.get("DB_USERNAME")}:{os.environ.get("DB_PASSWORD")}@{os.environ.get("DB_HOST")}/{os.environ.get("DB_NAME")}?driver=ODBC+Driver+17+for+SQL+Server')

class Database:

    @staticmethod
    def execute_query(query: str, params: dict = None, fetchone: bool = True):
        """Executes a query and returns a single row or None."""
        with engine.connect() as conn:
            result = conn.execute(text(query), params)
            if fetchone:
                return result.fetchone()
            else:
                return result.fetchall()

    @staticmethod
    def execute_update(query: str, params: dict):
        """Executes an update query and commits the transaction."""
        with engine.connect() as conn:
            conn.execute(text(query), params)
            conn.commit()
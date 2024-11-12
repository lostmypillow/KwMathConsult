from fastapi import FastAPI
from sqlalchemy import create_engine, text
import os
from classes.cardholder import Cardholder
app = FastAPI()

engine = create_engine(
    f'mssql+pyodbc://{os.environ.get("DB_USERNAME")}:{os.environ.get("DB_PASSWORD")}@{os.environ.get("DB_HOST")}/{os.environ.get("DB_NAME")}?driver=ODBC+Driver+17+for+SQL+Server')




def device_has_teacher(device_id: int) -> bool:
    query = """
    IF NOT EXISTS (
        SELECT 1
        FROM dbo.設備資料
        WHERE 設備號碼 = :device_id
        AND 老師編號 IS NOT NULL
    )
    BEGIN
        SELECT '沒輔導老師' AS Message;
    END
    ELSE
    BEGIN
        SELECT '有輔導老師' AS Message;
    END
    """
    with engine.connect() as conn:
        result = conn.execute(text(query), {'device_id': device_id}).fetchone()
    return True if result.Message == '有輔導老師' else False


def get_teacher_id(device_id: str) -> int:
    query = "SELECT 老師編號 FROM dbo.設備資料 WHERE 設備號碼 = :device_id"
    with engine.connect() as conn:
        result = conn.execute(text(query), {'device_id': device_id}).fetchone()
    conn.close()
    return result.老師編號


def register_teacher(teacher_id: int, device_id: int):
    select_query = "SELECT 設備號碼 FROM dbo.設備資料 WHERE 老師編號 = :teacher_id"
    update_query = "UPDATE dbo.設備資料 SET 老師編號 = :teacher_id WHERE 設備號碼 = :device_id"
    clear_query = "UPDATE dbo.設備資料 SET 老師編號 = NULL WHERE 設備號碼 = :existing_id"
    with engine.connect() as conn:
        existing_id = conn.execute(
            text(select_query), {'teacher_id': teacher_id}).fetchone()
        if not existing_id:
            conn.execute(text(update_query), {
                         'teacher_id': teacher_id, 'device_id': device_id})
            print('existing id does not exist, update')
        else:
            if existing_id.設備號碼 != int(device_id):
                conn.execute(text(clear_query), {
                             'existing_id': existing_id.設備號碼})
                conn.execute(text(update_query), {
                             'teacher_id': teacher_id, 'device_id': device_id})
            else:
                conn.execute(text(clear_query), {
                             'existing_id': existing_id.設備號碼})
        conn.commit()
        conn.close()


def register_student(student_id, teacher_id):
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
    with engine.connect() as conn:
        reservation_id = conn.execute(text(reservation_query), {
                                      'student_id': student_id, 'teacher_id': teacher_id}).fetchone()
        if not reservation_id:
            conn.execute(text(insert_query), {
                         'student_id': student_id, 'teacher_id': teacher_id})
            conn.commit()
        else:
            conn.execute(text(update_query), {
                         'reservation_id': reservation_id.自動編號})
            conn.commit()


@app.get('/{device_id}/{card_id}')
def process_card(card_id: str, device_id: int):
    cardholder = Cardholder(card_id)
    if cardholder.is_teacher:
        register_teacher(cardholder.id, device_id)
        return {'message': f'{cardholder.name}老師 刷卡成功'}
    elif cardholder.is_student:
        if device_has_teacher(device_id):
            register_student(cardholder.id, get_teacher_id(device_id))
            return {'message': f'{cardholder.name}同學 刷卡成功'}
        else:
            return {'message': '刷卡失敗: 輔導老師未刷卡'}
    else:
        return {'message': '刷卡失敗: 查無卡號'}



@app.get('/healthcheck')
def check_health():
    return {'message': 'server ok'}

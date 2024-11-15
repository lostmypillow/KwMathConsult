from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
def test_noteacher():
    response = client.get("/1/4600c81b6b")
    assert response.status_code == 200
    assert response.text == '刷卡失敗: 輔導老師未刷卡'
def test_teacher_then_student():
    response = client.get("/1/4600c86d17")
    assert response.status_code == 200
    assert response.text == "龍美如老師 刷卡成功"
    response = client.get("/1/4600c81b6b")
    assert response.status_code == 200
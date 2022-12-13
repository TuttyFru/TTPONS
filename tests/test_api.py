from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app, get_db
from src.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)  # Удалем таблицы из БД
Base.metadata.create_all(bind=engine)  # Создаем таблицы в БД

def override_get_db():
    """
    Данная функция при тестах будет подменять функцию get_db() в main.py.
    Таким образом приложение будет подключаться к тестовой базе данных.
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db  # Делаем подмену

client = TestClient(app)  # создаем тестовый клиент к нашему приложению



def test_create_workshop():
    """
    Тест на создание нового цеха
    """
    response = client.post(
        "/workshop/",
        json={"name": "Металургический цех", "full_name": "Лобанов Арнольд Еремеевич"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Металургический цех"

def test_get_workshop():
    """
    Тест на получение списка цехов из БД
    """
    response = client.get("/workshop/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["name"] == "Металургический цех"

def test_get_workshop_by_id():
    """
    Тест на получение цеха из БД по его id
    """
    response = client.get("/workshop/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Металургический цех"

def test_workshop_not_found():
    """
    Проверка случая, если цеха с таким id отсутствует в БД
    """
    response = client.get("/workshop/2")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Workshop not found"


def test_add_worker_to_workshop():
    """
    Тест на добавление работника цеху
    """
    response = client.post(
        "/workshop/1/workers/",
        json={"full_name": "Ширяев Зиновий Денисович", "job_title": "Охрана", "discount": 30}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["full_name"] == "Ширяев Зиновий Денисович"
    assert data["job_title"] == "Охрана"
    assert data["discount"] == 30
    assert data["job_id"] == 1

def test_get_workers():
    """
    Тест на получение списка работников из БД
    """
    response = client.get("/worker/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["full_name"] == "Ширяев Зиновий Денисович"
    assert data[0]["job_title"] == "Охрана"
    assert data[0]["discount"] == 30
    assert data[0]["job_id"] == 1

def test_get_worker_by_id():
    """
    Тест на получение цеха из БД по его id
    """
    response = client.get("/worker/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["full_name"] == "Ширяев Зиновий Денисович"

def test_worker_not_found():
    """
    Проверка случая, если работника с таким id отсутствует в БД
    """
    response = client.get("/workers/2")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Not Found"



def test_create_overall():
    """
    Тест на создание новой спецодежды
    """
    response = client.post(
        "/overall/",
        json={"kind": "Тапки", "wear_time": 3, "cost": 500}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["kind"] == "Тапки"

def test_get_overall():
    """
    Тест на получение списка спецодежды из БД
    """
    response = client.get("/overall/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["kind"] == "Тапки"
    assert data[0]["wear_time"] == 3
    assert data[0]["cost"] == 500

def test_get_overall_by_id():
    """
    Тест на получение спецодежды из БД по его id
    """
    response = client.get("/overall/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["kind"] == "Тапки"

def test_overall_not_found():
    """
    Проверка случая, если спецодежды с таким id отсутствует в БД
    """
    response = client.get("/overalls/2")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Not Found"


def test_add_worker_overall_to_reciving():
    """
    Тест на добавление работника и спецодежды получению
    """
    response = client.post(
        "/worker/1/overall/1/",
        json={
            "date": "11.12.13", 
            "signature": "Шир", 
            "worker_id": 1,
            "overall_id": 1
        }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["date"] == "11.12.13"
    assert data["signature"] == "Шир"
    assert data["worker_id"] == 1
    assert data["overall_id"] == 1

def test_get_reciving():
    """
    Тест на получение списка получений из БД
    """
    response = client.get("/reciving/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["date"] == "11.12.13"
    assert data[0]["signature"] == "Шир"
    assert data[0]["worker_id"] == 1
    assert data[0]["overall_id"] == 1

def test_get_reciving_by_id():
    """
    Тест на получение получений из БД по его id
    """
    response = client.get("/reciving/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["date"] == "11.12.13"

def test_reciving_not_found():
    """
    Проверка случая, если получение с таким id отсутствует в БД
    """
    response = client.get("/recivings/2")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Not Found"
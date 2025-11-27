import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from microservices_project.review_service.app.main import app
from microservices_project.review_service.app.database import Base, get_db
from microservices_project.review_service.app import models

TEST_DB_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DB_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)

# создание нового отзыва
def test_create_review():
    review_data = {
        "user_id": "11111111-1111-1111-1111-111111111111",
        "product_id": "22222222-2222-2222-2222-222222222222",
        "rating": 5,
        "comment": "Отличный товар!"
    }

    response = client.post("/api/reviews", json=review_data)
    assert response.status_code == 200

# получение всех отзывов
def test_get_reviews():
    response = client.get("/api/reviews/22222222-2222-2222-2222-222222222222")
    assert response.status_code == 200

# удаление существующего отзыва
def test_delete_review():
    response = client.get("/api/reviews/22222222-2222-2222-2222-222222222222")
    review_id = response.json()[0]["id"]

    response = client.delete(f"/api/reviews/{review_id}")
    assert response.status_code == 200

# сервис возвращает несколько отзывов для одного товара
def test_multiple_reviews_for_same_product():
    client.post("/api/reviews", json={
        "user_id": "11111111-1111-1111-1111-111111111111",
        "product_id": "prod-multi-1",
        "rating": 4,
        "comment": "Нормально"
    })

    client.post("/api/reviews", json={
        "user_id": "22222222-2222-2222-2222-222222222222",
        "product_id": "prod-multi-1",
        "rating": 5,
        "comment": "Отлично"
    })
    response = client.get("/api/reviews/prod-multi-1")
    data = response.json()
    assert len(data) == 2
    assert {review["rating"] for review in data} == {4, 5}

# отзыв можно создать без комментария
def test_create_review_without_comment():
    review_data = {
        "user_id": "abcabcab-abca-abca-abca-abcabcabcabc",
        "product_id": "commentless-product",
        "rating": 5,
        "comment": None
    }
    response = client.post("/api/reviews", json=review_data)
    assert response.status_code == 200

    data = response.json()
    assert data["comment"] is None
    assert data["rating"] == 5

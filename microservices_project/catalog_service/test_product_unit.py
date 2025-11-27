import os
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
from app2.models import Product
from uuid import uuid4
import pytest

@pytest.fixture
def sample_product():
    return Product(
        id=uuid4(),
        name="Пицца Маргарита",
        price=450.0,
        category="pizza",
        rating=4.5
    )

def test_product_creation(sample_product):
    assert sample_product.name == "Пицца Маргарита"
    assert sample_product.price == 450.0
    assert sample_product.category == "pizza"
    assert sample_product.rating == 4.5

def test_product_price_type(sample_product):
    assert isinstance(sample_product.price, float)

def test_product_default_rating():
    product = Product(id=uuid4(), name="Сок", price=150.0, category="drinks")
    assert product.rating == 0

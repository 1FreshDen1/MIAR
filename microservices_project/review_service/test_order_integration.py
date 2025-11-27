# import os
# import sys
# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from uuid import uuid4
#
# current_dir = os.path.dirname(__file__)
# project_root = os.path.abspath(os.path.join(current_dir, "../.."))  # microservices_project/
# sys.path.insert(0, project_root)
#
# from microservices_project.review_service import Base, Review
#
# DATABASE_URL = "sqlite:///./test.db"
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# @pytest.fixture(scope="module")
# def db():
#     Base.metadata.create_all(bind=engine)
#     db = TestingSessionLocal()
#     yield db
#     db.close()
#     Base.metadata.drop_all(bind=engine)
#
# def test_create_review(db):
#     new_review = Review(
#         id=uuid4(),
#         user_id=uuid4(),
#         product_id=uuid4(),
#         rating=4.5,
#         comment="Отличный товар!"
#     )
#     db.add(new_review)
#     db.commit()
#
#     result = db.query(Review).filter(Review.id == new_review.id).first()
#
#     assert result is not None
#     assert result.rating == 4.5
#     assert result.comment == "Отличный товар!"
#
# def test_update_review_comment(db):
#     review = db.query(Review).first()
#     review.comment = "Комментарий обновлён"
#     db.commit()
#
#     updated = db.query(Review).filter(Review.id == review.id).first()
#     assert updated.comment == "Комментарий обновлён"
#
#
# def test_update_review_rating(db):
#     review = db.query(Review).first()
#     review.rating = 3.0
#     db.commit()
#
#     updated = db.query(Review).filter(Review.id == review.id).first()
#     assert updated.rating == 3.0

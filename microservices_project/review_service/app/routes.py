from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database, rabbitmq
import asyncio
from uuid import uuid4

router = APIRouter()   # ← ДОЛЖНО БЫТЬ ПЕРЕД ДЕКОРАТОРАМИ!

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/api/reviews", response_model=schemas.ReviewResponse)
async def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    data = review.model_dump()

    new_review = models.Review(
        id=str(uuid4()),
        user_id=str(data["user_id"]),
        product_id=str(data["product_id"]),
        rating=data["rating"],
        comment=data.get("comment")
    )

    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    asyncio.create_task(rabbitmq.send_review_message({
        "review_id": new_review.id,
        "product_id": new_review.product_id,
        "rating": new_review.rating
    }))

    return new_review


@router.get("/api/reviews/{product_id}", response_model=list[schemas.ReviewResponse])
def get_reviews(product_id: str, db: Session = Depends(get_db)):
    return db.query(models.Review).filter(models.Review.product_id == product_id).all()


@router.delete("/api/reviews/{review_id}")
def delete_review(review_id: str, db: Session = Depends(get_db)):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review)
    db.commit()
    return {"message": "Review deleted"}

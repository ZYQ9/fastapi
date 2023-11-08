from sqlalchemy.orm import Session
from . import models, schemas 

def get_food(db: Session):
    return db.query(models.Food).all()

def get_food_by_id(db: Session, id: int):
    return db.query(models.Food).filter(models.Food.id == id).first()

def create_food(db: Session, food: schemas.Food):
    db_food = models.Food(id=food.id, name=food.name, price=food.price)
    db.add(db_food)
    db.commit()
    db.refresh(db_food)
    return db_food


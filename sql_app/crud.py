from sqlalchemy.orm import Session
from . import models, schemas 

def get_food(db: Session):
    return db.query(models.Food).all()

def create_food(db: Session, food: schemas.Food):
    db_food = models.Food(id=food.id, name=food.name, price=food.price)
    db.add(db_food)
    db.commit()
    db.refresh(db_food)
    return db_food
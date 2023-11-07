from sqlalchemy.orm import Session
from . import models, schemas 

def get_food(db: Session):
    return db.query(models.Food).all()
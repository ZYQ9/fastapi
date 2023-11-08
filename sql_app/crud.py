from sqlalchemy.orm import Session
from . import models, schemas 

# Food table functions
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

# Stores table functions
def get_stores(db: Session):
    return db.query(models.Stores).all()

def get_store_by_id(db: Session, id: int):
    return db.query(models.Stores).filter(models.Stores.id == id).first()


# Join table functions
def get_inventory_by_store(db: Session, id: int):
    db_inv = db.query(models.Stores).join(models.Join).filter(models.Stores.id == id).first()

    store_resp = schemas.StoreResponse(id=db_inv.id, name=db_inv.name, state=db_inv.state)

    return store_resp
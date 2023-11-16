from sqlalchemy.orm import Session
from . import models, schemas 

#---------------------------------
# Food table functions
#---------------------------------

#* GET Functions
def get_food(db: Session):
    return db.query(models.Food).all()

def get_food_by_id(db: Session, id: int):
    return db.query(models.Food).filter(models.Food.id == id).first()

#* POST Functions
def create_food(db: Session, food: schemas.Food):
    db_food = models.Food(id=food.id, name=food.name, price=food.price)
    db.add(db_food)
    db.commit()
    db.refresh(db_food)
    return db_food

#* PATCH Functions
def modify_food_price(db: Session, name: str, price: str):
    price_change = db.query(models.Food).filter(models.Food.name == name).first()
    price_change.price = price
    db.commit()
    return price_change

#* DELETE Functions
def delete_food(db: Session, id: int):
    food = db.query(models.Food).filter(models.Food.id == id).first()
    db.delete(food)
    db.commit()

#---------------------------------
# Store table functions
#---------------------------------

#* GET Functions
def get_stores(db: Session):
    return db.query(models.Stores).all()

def get_store_by_id(db: Session, id: int):
    return db.query(models.Stores).filter(models.Stores.id == id).first()

#* POST Functions
def create_store(db: Session, store: schemas.Store):
    db_store = models.Stores(id=store.id, name=store.name, state=store.state)
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store

#* DELETE Functions
def delete_store(db: Session, id: int):
    store = db.query(models.Stores).filter(models.Stores.id == id).first()
    db.delete(store)
    db.commit()

#---------------------------------
# Inventory table functions
#---------------------------------

#* GET Functions
def get_inventory_by_store(db: Session, id: int):
    db_inv = db.query(models.Stores).join(models.Join).filter(models.Stores.id == id).first()

    store_resp = schemas.StoreResponse(id=db_inv.id, name=db_inv.name, state=db_inv.state, stores=db_inv.join_stores )

    return store_resp

def get_inventory_all(db: Session):
    return db.query(models.Join).all()

#* POST Functions
def add_inventory(db: Session, inv: schemas.Join):
    add_inv = models.Join(store_id=add_inv.store_id, food_id=add_inv.food_id, inventory=add_inv.inventory)
    db.add(add_inv)
    db.commit()
    db.refresh(add_inv)
    return add_inv

#* PATCH Functions
def update_inventory(db: Session, store_id: int, food_id: int, inventory: int):
    update_inv = db.query(models.Join).filter((models.Join.store_id == store_id)&(models.Join.food_id == food_id)).first()
    update_inv.inventory = inventory
    db.commit()
    return update_inv

#* DELETE Functions
def remove_inventory(db:Session, store_id: int, food_id: int):
    inventory = db.query(models.Join).filter((models.Join.store_id == store_id)&(models.Join.food_id == food_id)).first()
    db.delete(inventory)
    db.commit()
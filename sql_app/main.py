from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API request to get food 
@app.get("/food", response_model=list[schemas.Food])
async def read_food(db: Session = Depends(get_db)):
    food = crud.get_food(db)
    return food

# API request to create food
@app.post("/food", response_model=schemas.Food,status_code=201)
async def create_food(
    food: schemas.Food,
    db: Session = Depends(get_db)
):
    """
    This section checks to see if the id for the food item exists 
    if it does, returns an error code.
    """
    db_food = crud.get_food_by_id(db, id=food.id)
    if db_food:
        raise HTTPException(status_code=400, detail="Food item exists")
    
    return crud.create_food(db=db, food=food)

# API request to get inventory by store
@app.get("/inventory/store/{id}", response_model=schemas.StoreResponse)
async def get_inventory_by_store(
    id: int,
    db: Session = Depends(get_db)
):
    return crud.get_inventory_by_store(db, id=id)


from fastapi import Depends, FastAPI, HTTPExeception
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

@app.get("/food", response_model=list[schemas.Food])
async def read_food(db: Session = Depends(get_db)):
    food = crud.get_food(db)
    return food


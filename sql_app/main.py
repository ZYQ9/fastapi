from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

import logging
import uvicorn

#! Authentication imports

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

# Secret Key to sign JWT 
SECRET_KEY = "cbbb848386d99f1b473a5f7748d878dae371fb6dca54cbd8e0fb7555b3fd27eb"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Fake DB
# TODO: Remove this later

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "",
        "disabled": False
    }
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")


models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Testing-App")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return schemas.UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth_2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username)
    if user is None:
        raise credentials_exception
    return user

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------------------------------------------
# Food API Endpoints
# -----------------------------------------------------------------

# API request to get food 
@app.get("/food", response_model=list[schemas.Food])
async def read_food(
    #token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)):
    food = crud.get_food(db)
    return food

@app.get("/")
async def read_root():
    return ("Hello World")

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

# API request to modify price of food
@app.patch("/food/{food_name}", response_model=schemas.Food, status_code=201)
async def modify_price(
    food_name,
    price: str,
    db: Session = Depends(get_db)
):
    return crud.modify_food_price(db, food_name, price)

# API request to delete a food item
@app.delete("/food/{food_id}", status_code=204)
async def delete_food(
    food_id,
    db: Session = Depends(get_db)
):
    crud.delete_food(db, food_id)

# -----------------------------------------------------------------
# Store API Endpoints
# -----------------------------------------------------------------

@app.get("/store", response_model=list[schemas.Store])
async def get_stores(db: Session = Depends(get_db)):
    store = crud.get_stores(db)
    return store

@app.get("/store/{id}", response_model=schemas.Store, status_code=201)
async def get_stores_by_id(
    id: int,
    db: Session = Depends(get_db)
):
    return crud.get_store_by_id(db,id)

@app.post("/store", response_model=schemas.Store, status_code=201)
async def create_store(
    store: schemas.Store,
    db: Session = Depends(get_db)
):
    db_store = crud.get_store_by_id(db, id=store.id)
    if db_store:
        raise HTTPException(status_code=400, detail="Store item exists")
    
    return crud.create_store(db=db, store=store)

@app.delete("/store/{store_id}", status_code=204)
async def delete_store(
    store_id,
    db: Session = Depends(get_db)
):
    crud.delete_store(db, store_id)

# -----------------------------------------------------------------
# Inventory API Endpoints
# -----------------------------------------------------------------

# API request to get inventory by store
@app.get("/inventory/store/{id}", response_model=schemas.StoreResponse)
async def get_inventory_by_store(
    id: int,
    db: Session = Depends(get_db)
):
    return crud.get_inventory_by_store(db, id=id)
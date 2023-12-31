from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

#? OpenTelemetry imports

import logging
import uvicorn
from azure.monitor.opentelemetry import configure_azure_monitor

from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
# configure_azure_monitor(connection_string=f'InstrumentationKey=1345b0d1-2330-4086-bc37-f378ee010f5a')

exporter = AzureMonitorTraceExporter.from_connection_string(
    "InstrumentationKey=1345b0d1-2330-4086-bc37-f378ee010f5a"
)
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(exporter))

logging.basicConfig(level=logging.DEBUG)
#! Authentication imports
# from typing import Annotated
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# from jose import JWTError, jwt
# from passlib.context import CryptContext

# # Secret Key to sign JWT 
# SECRET_KEY = "test-secret-key"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# # # Fake DB
# # # TODO: Remove this later

# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "labadmin123",
#         "disabled": False,
#     }
# }

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Testing-App")

FastAPIInstrumentor.instrument_app(app)
# @app.on_event("startup")
# def startup_event():

# Authentication requirements
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# def fake_decode_token(token):
#     return schemas.User(
#         username=token + "fakedecoded", email = "earl@example.com", full_name = "Earl OConnor"
#     )

# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     user = fake_decode_token(token)
#     return user

# @app.get("/user")
# async def read_users_me(current_user: Annotated[schemas.User, Depends(get_current_user)]):
#     return current_user

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
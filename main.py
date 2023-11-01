from fastapi import FastAPI 
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str


# Creates the root directory, this is required
@app.get("/")
async def root():
    return {"message":"Hello World"}

@app.get("/test/{test_id}")
async def read_item(test_id: int):
    return {"test_id": test_id}

fake_items = [{"name" : "Rick"},{"name" : "Morty"},{"name" : "Summer"},{"name" : "Beth"},{"name" : "Jerry"}]

@app.get("/name/")
async def read_item(skip: int = 0,limit: int = 10):
    return fake_items[skip:skip+limit]

@app.get("/list/")
async def read_item():
    for keys,value in fake_items.items():
        return fake_items.items()
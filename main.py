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

@app.put("/name/{name_id}")
async def create_item(name_id: int, fake_items: Item):
    return {"item_id": name_id, **fake_items.dict()}
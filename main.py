from fastapi import FastAPI 
from pydantic import BaseModel

class Item(BaseModel):
    name: str

app = FastAPI()

fake_items = [{"name" : "Rick"},{"name" : "Morty"},{"name" : "Summer"},{"name" : "Beth"},{"name" : "Jerry"}]

# Creates the root directory
@app.get("/")
async def root():
    return {"message":"Hello World"}

@app.get("/test/{test_id}")
async def read_item(test_id: int):
    return {"test_id": test_id}

@app.get("/name")
async def read_item():
    return fake_items

@app.get("/list/{list_item}")
async def read_item(list_item: int):
    return fake_items[list_item]

@app.post("/post")
async def create_item(item: Item)
    return item

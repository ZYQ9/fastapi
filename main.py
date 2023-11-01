from fastapi import FastAPI 
from pydantic import BaseModel

app = FastAPI()

fake_items = [{"name" : "Rick"},{"name" : "Morty"},{"name" : "Summer"},{"name" : "Beth"},{"name" : "Jerry"}]

# Creates the root directory
@app.get("/")
async def root():
    return {"message":"Hello World"}

@app.get("/test/{test_id}")
async def read_item(test_id: int):
    return {"test_id": test_id}

@app.get("/name/")
async def read_item(skip: int = 0,limit: int = 10):
    return fake_items[skip:skip+limit]

@app.get("/list/{list_item}")
async def read_item(list_item: int | None = None):
    return fake_items[list_item]

@app.post("/put/{put_item}")
async def create_item(put_item:str)
    fake_items["name"].append(put_item)

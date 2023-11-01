from fastapi import FastAPI 

app = FastAPI()

# Creates the root directory, this is required
@app.get("/")
async def root():
    return {"message":"Hello World"}

@app.get("/test/{test_id}")
async def read_item(test_id: int):
    return {"test_id": test_id}

fake_items = [{"name" : "Rick"},{"name" : "Morty"},{"name" : "Summer"},{"name" : "Beth"},{"name" : "Jerry"}]

@app.get("/name/")
async def read_item(skip,limit):
    return fake_items[skip:skip+limit]
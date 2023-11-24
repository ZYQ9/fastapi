from pydantic import BaseModel, ConfigDict

# Authentication Schemas

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


# DB Schemas
class FoodBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
    
    id: int
    
    
class Food(FoodBase):
    
    name: str
    price: str

class StoreBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
    
    id: int 
    

class Store(StoreBase):
    
    name: str
    state: str

class JoinBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    store_id: int
    food_id: int

class Join(JoinBase):
    inventory: int

class StoreResponse(Store):
    stores: list[Join]
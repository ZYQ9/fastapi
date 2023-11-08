from pydantic import BaseModel, ConfigDict

class FoodBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
    
    name: str
    
class Food(FoodBase):
    id: int
    price: str

class StoreBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
    
    name: str

class Store(StoreBase):
    id: int 
    state: str

class JoinBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    store_id: int
    food_id: int

class Join(JoinBase):
    inventory: int

class StoreResponse(Store):
    stores: list[Join]

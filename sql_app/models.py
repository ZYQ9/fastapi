from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .database import Base

class Food(Base):
    __tablename__ = "food"

    id: Mapped[Integer] = mapped_column(primary_key=True)
    name: Mapped[String] = mapped_column()
    price: Mapped[String] = mapped_column()



class Stores(Base):
    __tablename__ = "stores"

    id: Mapped[Integer] = mapped_column(primary_key=True)
    name: Mapped[String] = mapped_column()
    state: Mapped[String] = mapped_column()

class Join(Base):
    __tablename__ = "join"

    store_id: Mapped[Integer] = mapped_column(primary_key=True, ForeignKey("stores.id"))
    food_id: Mapped[Integer] = mapped_column(primary_key=True, ForeignKey("food.id"))
    inventory: Mapped[Integer] = mapped_column()

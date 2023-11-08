from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .database import Base

class Food(Base):
    __tablename__ = "food"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    price: Mapped[str] = mapped_column()

    join_food: Mapped[list["Join"]] = relationship(back_populates="food")


class Stores(Base):
    __tablename__ = "stores"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    state: Mapped[str] = mapped_column()

    join_stores: Mapped[list["Join"]] = relationship(back_populates="stores")

class Join(Base):
    __tablename__ = "join"

    store_id: Mapped[int] = mapped_column( ForeignKey("stores.id"),primary_key=True)
    food_id: Mapped[int] = mapped_column(ForeignKey("food.id"),primary_key=True)
    inventory: Mapped[int] = mapped_column()

    food: Mapped[list["Food"]] = relationship(back_populates="join_food")
    stores: Mapped[list["Stores"]] = relationship(back_populates="join_stores")


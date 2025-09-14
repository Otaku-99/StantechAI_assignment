from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class ItemBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    price: float = Field(..., ge=0)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)


class ItemOut(ItemBase):
    id: int
    created_at: datetime


class Config:
    orm_mode = True
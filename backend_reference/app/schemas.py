from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ProductCreate(BaseModel):
    name: str
    description: str = ""
    price: float
    stock: int = 0


class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    price: float
    stock: int


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = 1


class OrderCreate(BaseModel):
    items: list[OrderItemCreate]


class OrderItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
    quantity: int
    unit_price: float


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    items: list[OrderItemOut]

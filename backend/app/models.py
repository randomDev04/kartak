from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Item(Base):
    __tablename__ = "items"
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    name:Mapped[str] = mapped_column(String(100))
    price:Mapped[float] = mapped_column()
    in_stock:Mapped[bool] = mapped_column(default=True)
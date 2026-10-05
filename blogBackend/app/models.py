from sqlalchemy import Column, Integer, String, Text
from app.database import Base

# Define your models here
# For example, a simple User model could look like this:
class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
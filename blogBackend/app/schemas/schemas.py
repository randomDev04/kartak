from pydantic import BaseModel

# Input Schemas
class BlogCreate(BaseModel):
    title: str
    content: str

# Output Schemas
class BlogResponse(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True
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

class BlogListResponse(BaseModel):
    total: int
    page: int
    limit: int
    data: list[BlogResponse]

    class Config:
        from_attributes = True
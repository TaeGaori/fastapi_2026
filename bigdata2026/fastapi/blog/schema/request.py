from pydantic import BaseModel

class PostCreateRequest(BaseModel):
    title: str
    content: str

class PostUpdateRequest(BaseModel):
    title: str  |None = None
    content: str |None = None
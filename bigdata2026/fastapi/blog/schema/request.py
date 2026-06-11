from pydantic import BaseModel

class PostCreateRequest(BaseModel):
    title: str

class PostUpdateRequest(BaseModel):
    title: str
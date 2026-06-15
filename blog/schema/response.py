from pydantic import BaseModel

class Postresponse(BaseModel):
    id : int
    title : str
    content : str
from pydantic import BaseModel

class User(BaseModel):
    token: str
    name: str
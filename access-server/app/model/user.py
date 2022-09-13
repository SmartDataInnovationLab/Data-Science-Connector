from pydantic import BaseModel

class UserRequest(BaseModel):
    name: str

class User(UserRequest):
    token: str
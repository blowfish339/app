from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class User(UserBase):
    password: str

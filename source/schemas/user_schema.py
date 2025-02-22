from pydantic import BaseModel

class UserLoginSchema(BaseModel):
    email: str
    password: str

class UserSchema(UserLoginSchema):
    name: str
    phone: str
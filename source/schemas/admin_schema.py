from pydantic import BaseModel

class AdminSchema(BaseModel):
    email: str
    password: str
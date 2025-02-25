from pydantic import BaseModel

class SellerLoginSchema(BaseModel):
    email: str
    password: str

class SellerSchema(SellerLoginSchema):
    name: str
    phone: str
    store: str
    category: str
    
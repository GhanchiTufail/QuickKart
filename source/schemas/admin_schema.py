from pydantic import BaseModel

class AdminSchema(BaseModel):
    email: str
    password: str

# updated 

class SellerPagination(BaseModel):
    limit: int | None = 10
    page: int | None = 1
    category: str | None = None
    store: str | None = None
    phone: str | None = None
    name: str | None = None
    email: str | None = None
    

class SellerList():
    pass

class SellerListResponse(BaseModel):
    name: str
    email: str
    phone: str
    store_name: str
    category: str

class UserPagination(BaseModel):
    limit: int | None = 10
    page: int | None = 1
    name: str | None = None
    email: str | None = None
    phone: str | None = None
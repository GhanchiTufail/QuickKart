from fastapi import Form
from typing import Optional
from pydantic import BaseModel

class ProductSchema(BaseModel):
    name: str
    description: str
    price: float
    category: str
    stock: int
    is_rentable: bool = False
    daily_rate: Optional[float] = 0.0
    brand: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        description: str = Form(...),
        price: float = Form(...),
        category: str = Form(...),
        stock: int = Form(...),
        is_rentable: bool = Form(False),
        daily_rate: Optional[float] = Form(0.0),
        brand: Optional[str] = Form(None),
    ):
        return cls(
            name=name,
            description=description,
            price=price,
            category=category,
            stock=stock,
            is_rentable=is_rentable,
            daily_rate=daily_rate,
            brand=brand,
        )
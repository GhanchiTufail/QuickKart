from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from source.schemas.product_schema import ProductSchema
from source.config.database import get_db
from source.utils.token import get_current_seller
from source.modules.seller.seller_controller import login_seller_controller, create_seller_controller
from source.models.seller import Seller
from source.models.product import Product
from source.utils.categories import CategoryEnum

router = APIRouter(prefix="/product", tags=["Product"])
templates = Jinja2Templates(directory="templates")

@router.post("/register")
def create_seller(request: Request, product : ProductSchema = Form(...), db: Session = Depends(get_db), seller : Seller = Depends(get_current_seller)):
    
    new_product = Product(
        name=product.name,
        description=product.description,
        image=product.image,
        price=product.price,
        category=seller.category,  # Auto-fill category from logged-in seller
        sub_category=product.category,
        stock=product.stock,
        is_rentable=product.is_rentable,
        daily_rate=product.daily_rate,
        brand=product.brand,
        seller_id=seller.id  # Auto-fill seller ID
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {"message": "Product added successfully!", "product_id": new_product.id}
    #return create_seller_controller(request, seller, db)
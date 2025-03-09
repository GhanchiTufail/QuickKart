from fastapi import Depends, Request
from sqlalchemy.orm import Session
from source.config.database import get_db
from source.models.seller import Seller
from source.models.product import Product
from source.utils.token import get_current_seller

#seller role
def get_seller_products(
    request: Request,
    db: Session = Depends(get_db),
    seller: Seller = Depends(get_current_seller)

):
    product = db.query(Product).filter(Product.seller_id == seller.id).all()   
    return product

def get_all_products(
    db: Session = Depends(get_db)
):
    product = db.query(Product).all()   
    return product
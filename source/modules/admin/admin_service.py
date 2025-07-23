from fastapi import Request, Depends, Form, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from source.config.database import get_db
from source.models.admin import Admin
from source.utils.hashing import verify_password, hash_password
from source.utils.token import create_access_token, get_current_admin
from source.schemas.admin_schema import AdminSchema, SellerPagination, UserPagination, ProductPagination
from source.models.seller import Seller
from source.models.user import User
from source.models.product import Product
from math import ceil
from source.utils.categories import CategoryEnum

templates = Jinja2Templates(directory="templates")


def create_admin_service(request: Request, admin: AdminSchema, db: Session):
    # try:
    #     query = db.query(Admin).filter(Admin.email == admin.email).first()
    #     if query:
    #         return False
    # except:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="error in checking if admin exist or not")
    
    new_admin = Admin(email=admin.email, password=hash_password(admin.password))
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return True


def login_admin_service(admin: AdminSchema = Form(...), db: Session = Depends(get_db)):
    try:
        admin_data = db.query(Admin).filter(Admin.email == admin.email).first()
        if admin_data and verify_password(admin.password, admin_data.password):
            access_token = create_access_token(admin.email, "admin")
            return access_token
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="error while creating admin token")

# updated
def seller_list_service(seller: SellerPagination,db: Session):
    query = db.query(Seller)
    # condition = []
    # if seller.category:
    #     condition.append(Seller.category == seller.category)
    # if seller.phone:
    #     condition.append(Seller.phone == seller.phone)
    # if seller.email:
    #     condition.append(Seller.email == seller.email)
    # if seller.name:
    #     condition.append(Seller.name == seller.name)
    # if seller.store:
    #     condition.append(Seller.store_name == seller.store)
    offset = (seller.page - 1) * seller.limit
    query = query.offset(offset).limit(seller.limit)
    query = query.with_entities(
        Seller.id,
        Seller.name,
        Seller.email,
        Seller.phone,
        Seller.store_name,
        Seller.category.label("category"),
        Seller.is_banned
    )
    # query = query.filter(*condition)
    total_seller = query.count()
    total_pages = ceil(total_seller / seller.limit)
    return query, seller.page,total_seller, total_pages

def  user_list_service(user: UserPagination,db: Session):
    query = db.query(User)
    condition = []
    # if user.phone:
    #     condition.append(User.phone == user.phone)
    # if user.email:
    #     condition.append(User.email == user.email)
    # if user.name:
    #     condition.append(User.name == user.name)
    offset = (user.page - 1) * user.limit
    # query = query.filter(*condition)
    total_user = query.count()
    total_pages = ceil(total_user / user.limit)
    query = query.offset(offset).limit(user.limit)
    query = query.with_entities(
        User.id,
        User.name,
        User.email,
        User.phone
    )
    return query,user.page,total_pages,total_user


def  product_list_service(product: ProductPagination,db: Session):
    status = None
    query = db.query(Product).join(Seller, Product.seller_id == Seller.id)
    if product.seller_id:
        status = db.query(Seller).filter(Seller.id == product.seller_id).first()
        if status.is_banned is True:
            status = "Activete Seller"
        elif status.is_banned is False:
            status = "Ban Seller"

    if product.seller_id:
        query = query.filter(Product.seller_id == product.seller_id)

    offset = (product.page - 1) * product.limit

    total_products = query.count()

    total_pages = ceil(total_products / product.limit)

    query = query.offset(offset).limit(product.limit)

    query = query.with_entities(
        Product.id,
        Product.name,
        Product.sub_category,
        Product.price,
        Product.stock,
        Seller.name.label("seller_name"),
        Product.image
    )   

    return {
        "query":query,
        "page":product.page,
        "total pages":total_pages,
        "total product":total_products,
        "status":status,
        "Seller id":product.seller_id if product.seller_id else None
    }


def seller_ban_service(seller_id:int, db: Session):
    query = db.query(Seller).filter(Seller.id == seller_id).first()
    if query.is_banned == False:
        query.is_banned = True
        message = "ban"
    else:
        query.is_banned = False
        message = "Activate"

    db.commit()
    db.refresh(query)

    return {"Message":f"{query.name} is now {message}"}

# def seller_unban_service(seller_id:int, db:Session):
#     query = db.query(Seller).filter(Seller.id == seller_id).first()
#     query.is_banned = False
#     db.commit()
#     db.refresh(query)
#     return {"Message":f"{query.name} is now unban"}
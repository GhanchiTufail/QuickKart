from fastapi import Request, Depends, Form, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from source.config.database import get_db
from source.models.admin import Admin
from source.utils.hashing import verify_password, hash_password
from source.utils.token import create_access_token, get_current_admin
from source.schemas.admin_schema import AdminSchema, SellerPagination, UserPagination
from source.models.seller import Seller
from source.models.user import User

templates = Jinja2Templates(directory="templates")


def create_admin_service(request: Request, admin: AdminSchema, db: Session):
    try:
        query = db.query(Admin).filter(Admin.email == admin.email).first()
        if query:
            return False
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="error in checking if admin exist or not")
    try:
        new_admin = Admin(email=admin.email, password=hash_password(admin.password))
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        return True
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in creating admin")


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
    condition = []
    if seller.category:
        condition.append(Seller.category == seller.category)
    if seller.phone:
        condition.append(Seller.phone == seller.phone)
    if seller.email:
        condition.append(Seller.email == seller.email)
    if seller.name:
        condition.append(Seller.name == seller.name)
    if seller.store:
        condition.append(Seller.store_name == seller.store)
    offset = (seller.page - 1) * seller.limit
    query = query.filter(*condition)
    total_user = query.count()
    query = query.offset(offset).limit(seller.limit)
    query = query.with_entities(
        Seller.id,
        Seller.name,
        Seller.email,
        Seller.phone,
        Seller.store_name,
        Seller.category,
        Seller.is_banned
    )
    return query,total_user

def user_list_service(user: UserPagination,db: Session):
    query = db.query(User)
    condition = []
    if user.phone:
        condition.append(User.phone == user.phone)
    if user.email:
        condition.append(User.email == user.email)
    if user.name:
        condition.append(User.name == user.name)
    offset = (user.page - 1) * user.limit
    query = query.filter(*condition)
    total_user = query.count()
    query = query.offset(offset).limit(user.limit)
    query = query.with_entities(
        User.id,
        User.name,
        User.email,
        User.phone
    )
    return query,total_user
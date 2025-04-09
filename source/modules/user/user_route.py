from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from source.schemas.user_schema import UserLoginSchema, UserSchema
from source.config.database import get_db
from source.utils.token import get_current_user
from source.modules.user.user_controller import login_user_controller, create_user_controller, add_to_cart_controller, show_cart_controller, order_controller, account_controller, cart_remove_controller, single_product_controller, rent_product_controller, get_order_controller, get_order_service, rental_list_controller, notification_list_controller
from source.models.user import User
from source.models.product import Product
from source.models.cart import Cart
from source.utils.dependency import get_all_products

router = APIRouter(prefix="/user", tags=["User"])
templates = Jinja2Templates(directory="templates")

@router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("user/user_gateway/signup.html", {"request": request})


@router.post("/register")
async def create_seller(request: Request, user: UserSchema = Form(...), db: Session = Depends(get_db)):
    return create_user_controller(request, user, db)


@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("user/user_gateway/login.html", {"request": request})


@router.post("/login")
async def login_seller(request: Request, user: UserLoginSchema = Form(...), db: Session = Depends(get_db)):
    return login_user_controller(request, user, db)


# User Dashboard
@router.get("/home")
async def user_dashboard(request: Request, user: User = Depends(get_current_user), product: Product = Depends(get_all_products)):
    return templates.TemplateResponse("user/home.html", {"request": request, "user":user, "product":product})

@router.post("/cart/{page}/{product_id}")
async def add_to_cart(request: Request, page:str, product_id: int,quantity: int = 1, user: User = Depends(get_current_user), product: Product = Depends(get_all_products), db: Session = Depends(get_db)):
    add_to_cart_controller(request,product_id,user.id,db,quantity)
    if page == "home":
        return RedirectResponse(url="/user/home", status_code=303)
    elif page == "product":
        return RedirectResponse(url="/user/product/{product_id}")


@router.get("/cart")
async def show_cart(request: Request, user: User = Depends(get_current_user), product: Product = Depends(get_all_products),db: Session = Depends(get_db)):
    query = db.query(Cart).filter(user.id == Cart.user_id).all()
    total = 0
    cart_list = []
    for i in query:
        total += i.amount
        prd = db.query(Product).filter( Product.id == i.product_id).first()
        cart_list.append({
                "cart_id": i.id,
                "product_name": prd.name,  # assuming field is named 'name'
                "product_image": prd.image,  # assuming field is named 'image'
                "product_description": prd.description,  # assuming field is named 'description'
                "quantity": i.quantity,  # adjust field name if needed
                "price": i.amount,
                "stock": prd.stock
        })
        # print(cart_list(1))
    # product = show_cart_controller(request,user, db)
    return templates.TemplateResponse("user/cart.html", {"request": request, "user":user, "cart":cart_list, "total":total})


@router.post("/checkout/{id}")
async def checkout(request: Request, id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    query = db.query(Cart).filter(user.id == Cart.user_id).all()
    cart_list = []
    total = 0
    for i in query:
        prd = db.query(Product).filter( Product.id == i.product_id).first()
        total += i.amount
        cart_list.append({
                "product_name": prd.name,  # assuming field is named 'name'
                "product_image": prd.image,  # assuming field is named 'image'
                "product_description": prd.description,  # assuming field is named 'description'
                "quantity": i.quantity,  # adjust field name if needed
                "price": i.amount 
        })
    return templates.TemplateResponse("user/checkout.html", {"request": request,"id":id, "user":user, "cart":cart_list, "total":total})


@router.post("/order/{id}")
async def order_route(request: Request, id: int,user: User = Depends(get_current_user), product: Product = Depends(get_all_products), db:Session=Depends(get_db)):
    order_controller(request,id,db)
    return {"message":"success"}
    return RedirectResponse("/user/home", status_code=303)


@router.get("/account")
async def account(request: Request,user:User = Depends(get_current_user), db: Session = Depends(get_db)):
    query = account_controller(request, user.id, db)
    return templates.TemplateResponse("user/account.html", {"request":request, "id":query.id, "name":query.name, "email":query.email, "phone":query.phone })


@router.post("/cart/{id}")
async def cart_remove(request: Request, id: int, db: Session = Depends(get_db)):
    cart_remove_controller(request, id, db)
    return RedirectResponse(url="/user/cart" , status_code=303)


@router.get("/product/{id}")
async def single_product_service(request: Request, id: int, db: Session = Depends(get_db)): 
    product = single_product_controller(request, id, db)
    print(product.is_rentable)
    return templates.TemplateResponse("user/product.html",{"request":request, "id":product.id, "image":product.image, "name":product.name, "price":product.price, "description":product.description, "rent":product.is_rentable, "stock":product.stock})


@router.get("/order")
async def order_list(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    product = get_order_service(user, db)
    return templates.TemplateResponse("user/Orderitem.html",{"request":request, "product":product})


@router.post("/rent/{id}")
async def rent(request: Request, id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    product = single_product_controller(request, id, db)
    return templates.TemplateResponse("user/rent.html", {"request":request,"id":product.id, "name":product.name, "price":product.daily_rate})


@router.post("/rent/item/{id}/{month}")
async def rent_item(request: Request, id: int,month: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rent_product_controller(request, id, month, user, db)
    return RedirectResponse(url="/user/home" , status_code=303)


@router.get("/rent")
async def rent_list(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    product = rental_list_controller(request, user, db)
    return templates.TemplateResponse("user/rent_item.html",{"request":request, "product":product})


@router.get("/notification")
async def notification_list(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    notification = notification_list_controller(request, user, db)
    return templates.TemplateResponse("user/notification.html", {"request":request, "notifications": notification})
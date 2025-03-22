from fastapi import APIRouter, Request, Depends, Form, UploadFile, File, HTTPException, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from cloudinary.uploader import upload
import cloudinary
from sqlalchemy.orm import Session
from source.schemas.seller_schema import SellerLoginSchema, SellerSchema
from source.config.database import get_db
from source.utils.token import get_current_seller
from source.modules.seller.seller_controller import login_seller_controller, create_seller_controller, product_delete_service, product_detail_service
from source.models.seller import Seller
from source.models.product import Product
from source.schemas.product_schema import ProductSchema
from source.utils.dependency import get_seller_products
from source.utils.upload import Configure
from source.utils.categories import ( 
    CategoryEnum,
    CATEGORY_MAPPING,
    ELECTRONICS,
    CLOTHING,
    BOOKS,
    HOME,
    BEAUTY,
    SPORTS,
    TOYS,
    HEALTH,
    GROCERIES,
    OFFICE,
    BABY,
    SHOES,
    JEWELRY,
    TOOLS,
    MOVIES
)

router = APIRouter(prefix="/seller", tags=["Seller"])
templates = Jinja2Templates(directory="templates")

@router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("seller/signup.html", {"request": request,"categories":list(CategoryEnum)})


@router.post("/register")
async def create_seller(request: Request, seller: SellerSchema = Form(...), db: Session = Depends(get_db)):
    return create_seller_controller(request, seller, db)


@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("seller/login.html", {"request": request})


@router.post("/login")
async def login_seller(request: Request, seller: SellerLoginSchema = Form(...), db: Session = Depends(get_db)):
    return login_seller_controller(request, seller, db)


# seller dashboard (protected)
@router.get("/home")
async def seller_dashboard(request: Request,seller: Seller = Depends(get_current_seller),product: Product = Depends(get_db)):
    return templates.TemplateResponse("seller/seller_dashboard.html",{"request": request, "seller": seller})
    


# seller profile (protected)
@router.get("/profile")
async def seller_profile(request: Request,seller: Seller = Depends(get_current_seller)):
    return templates.TemplateResponse("seller/seller_profile.html",{"request": request, "seller": seller})


# seller product
@router.get("/product")
async def seller_products(request: Request, seller: Seller = Depends(get_current_seller), products: Product = Depends(get_seller_products)):
    sub_category_enum = CATEGORY_MAPPING.get(seller.category)
    list = []
    for data in sub_category_enum:
        list.append(data)
    return templates.TemplateResponse("seller/seller_products.html",{"request":request, "seller":seller, "products":products, "categories":list})
    

@router.post("/product/add")
async def seller_products(
    request: Request,
    product: ProductSchema = Depends(ProductSchema.as_form),
    seller: Seller = Depends(get_current_seller),
    db: Session = Depends(get_db),
    image: UploadFile = File(...)
):
    cloudinary_result = upload(image.file)
    image_url = cloudinary_result.get("secure_url")

    new_product = Product(
        name=product.name,
        description=product.description,
        image=image_url,
        price=product.price,
        category=seller.category,  # Auto-fill category from logged-in seller
        sub_category=product.category,
        stock=product.stock,
        is_rentable=product.is_rentable,
        daily_rate=product.daily_rate,
        brand=product.brand,
        seller_id=seller.id
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return RedirectResponse(url="/seller/product", status_code=303)
    # return templates.TemplateResponse("seller/seller_products.html",{"request":request, "seller":seller})

# seller order
@router.get("/order")
async def seller_order(request: Request, seller: Seller = Depends(get_current_seller)):
    return templates.TemplateResponse("seller/seller_order.html",{"request":request,"seller":seller})


# seller analytics
@router.get("/analytics")
async def seller_analytics(request: Request, seller: Seller = Depends(get_current_seller)):
    return templates.TemplateResponse("seller/seller_analytics.html",{"request":request,"seller":seller})

@router.get("/product/add")
async def add_product(request: Request, seller: Seller = Depends(get_current_seller)):
    sub_category_enum = CATEGORY_MAPPING.get(seller.category)
    list = []
    for data in sub_category_enum:
        list.append(data)
    # return {"list":list}
    # subcategories = [item.value for item in sub_category_enum] if sub_category_enum else []
    # print(subcategories)
    # subcategories = []
    # for item in sub_category_enum:
    #     subcategories.append(item[])
    return templates.TemplateResponse("seller/seller_products.html",{"request":request,"seller":seller, "categories":list})



@router.get("/product/image/{product_id}")
async def get_product_image(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product or not product.image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    return Response(content=product.image, media_type="image/jpeg")

@router.get("")
def get_list():
    data = list[CategoryEnum]
    # for list in CategoryEnum:
    #     data.append(list)
    return {"list":data}


@router.post("/product/delete/{id}")
async def product_delete(id:int, db: Seller = Depends(get_db)):
    product_delete_service(id,db)
    return {"Message":"Successful"}


@router.get("/product/details/{id}")
async def product_details(id:int, db: Session = Depends(get_db)):
    return product_detail_service(id, db)
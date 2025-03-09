from fastapi import FastAPI
from source.modules.admin import admin_route
from source.modules.user import user_route
from source.modules.seller import seller_route

app = FastAPI()

app.include_router(admin_route.router)
app.include_router(user_route.router)
app.include_router(seller_route.router)
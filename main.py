from fastapi import FastAPI,staticfiles
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import Base,engine 
from app.api.v1.auth_routes import router as auth_router
from app.api.v1.users import router as user_router
from app.api.v1.products import router as product_router
from app.api.v1.variants import router as variant_router
from app.api.v1.orders import router as orders_router
from app.api.v1.cart import router as cart_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"], 
)
Base.metadata.create_all(bind=engine)

app.include_router(auth_router,prefix='/api/v1/auth',tags=['Authentication'])
app.include_router(user_router,prefix='/api/v1/users',tags=['Users'])
app.include_router(product_router,prefix='/api/v1/products',tags=['Products'])
app.include_router(variant_router,prefix="/api/v1/variants",tags=["variants"])
app.include_router(orders_router,prefix="/api/v1/orders",tags=["orders"])
app.include_router(cart_router,prefix="/api/v1/cart",tags=["cart"])


app.mount("/static" ,staticfiles.StaticFiles(directory="static"),name="static")

@app.get("/")
async def index():
   return {"message": "Welcome to our user management system"}

   

     
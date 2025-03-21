from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import Base,engine 
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as user_router
from app.api.v1.products import router as product_router


app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=['*'],
  allow_headers=['*'],
  allow_methods=['*']
)
Base.metadata.create_all(bind=engine)

app.include_router(auth_router,prefix='/api/v1/auth',tags=['Authentication'])
app.include_router(user_router,prefix='/api/v1/users',tags=['Users'])
app.include_router(product_router,prefix='/api/v1/products',tags=['Products'])


@app.get("/")
async def index():
   return {"message": "Welcome to our user management system"}

   

     
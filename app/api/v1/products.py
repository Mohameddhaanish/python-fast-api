from fastapi import APIRouter, Depends, UploadFile,File,HTTPException,Form
from sqlalchemy.orm import Session
import urllib3.util
from app.db.models import Product,Variant
from app.db.schemas import ProductResponse,VariantResponse,AllProductsResponse
from app.db.session import get_db
import cloudinary.uploader,cloudinary
from app.core.config import settings
import certifi
import urllib3
import tempfile
from typing import List

router = APIRouter()

cloudinary.config(
    cloud_name=settings.NEXT_CLOUDINARY_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    verify_ssl=False
)

urllib3.util.ssl_.DEFAULT_CA_BUNDLE_PATH = certifi.where()

async def uploadImage(imageFile: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            contents = await imageFile.read()
            tmp.write(contents)
            tmp.flush()
            result = cloudinary.uploader.upload(
                tmp.name,
                resource_type="image",
                folder="danimerce",
                verify=False
            )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image upload failed: {str(e)}")

@router.post("/", response_model=ProductResponse)
async def create_product(  title: str = Form(...),
    description: str = Form(...),
    sku: str = Form(...),
    in_stock: bool = Form(True),
    image_url: UploadFile = File(...),
    category_id:int=Form(...),
    stock:int=Form(...),
    price:float=Form(...),
    discounted_price:float=Form(...),
    db: Session = Depends(get_db),):

    try:
        upload=await uploadImage(image_url)
        if not upload :
           raise HTTPException(status_code=500,detail="Could not upload image")
        
        product_details = {
            "title": title,
            "description": description,
            "sku": sku,
            "in_stock": in_stock,
            "category_id":category_id,
            "image_url": upload["secure_url"],
            "public_id":upload["public_id"],
            "stock":stock,
            "price":price,
            "discounted_price":discounted_price
        }

        db_product = Product(**product_details)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)

        default_variant = Variant(
            name=title,
            product_id=db_product.id,
            price=price,
            stock=stock,
            color="default",
            discounted_price=discounted_price,
        )
        db.add(default_variant)
        db.commit()
        db.refresh(default_variant)

        return db_product
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create product: {str(e)}")
    
@router.get("/get_all_products", response_model=List[AllProductsResponse])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()

    response = []
    for product in products:
        default_variant = (
            db.query(Variant)
            .filter(Variant.product_id == product.id, Variant.is_default == True)
            .first()
        )

        response.append(AllProductsResponse(
            id=product.id,
            title=product.title,
            description=product.description,
            image_url=product.image_url,
            sku=product.sku,
            price=product.price,
            stock=product.stock,
            discounted_price=product.discounted_price,
            default_variant_id=default_variant.id if default_variant else None,
            in_stock=product.in_stock if hasattr(product, "in_stock") else True,
            public_id=product.public_id if hasattr(product, "public_id") else None
        ))

    return response


@router.get("/get_products_by_category/{category_id}",response_model=List[AllProductsResponse])
def get_all_products_y_categroy(category_id:int,db:Session=Depends(get_db)):
     products= db.query(Product).filter(Product.category_id == category_id)
     return [AllProductsResponse.model_validate(product) for product in products] 
    

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    variants = [
        VariantResponse(
            id=variant.id,
            product_id=variant.product_id,
            name=variant.name,
            price=variant.price,
            images=[img.image_url for img in variant.image_url],
            color=variant.color,
            stock=variant.stock,
            discounted_price=variant.discounted_price,
            is_default=variant.is_default
        ) for variant in product.variants
    ]

    return ProductResponse(
        id=product.id,
        title=product.title,  
        description=product.description,  
        image_url=product.image_url,  
        sku=product.sku, 
        in_stock=product.in_stock,  
        public_id=product.public_id, 
        category=product.category,
        variants=variants,
        price=product.price,
        stock=product.stock,
        discounted_price=product.discounted_price
    )

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db.query(Product).filter(Product.id == product_id).delete()
    db.commit()
    return {"message": "Product deleted"}




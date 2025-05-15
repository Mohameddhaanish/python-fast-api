from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.db.models import Product,ProductCategory,ProductInventory,ProductDiscount
from app.db.schemas import ProductCreate,ProductCategoryCreate,ProductInventoryCreate,ProductDiscountCreate
import os
import shutil
from fastapi import UploadFile
from typing import List,Optional

def save_images(images: List[UploadFile], upload_dir: str = "static/images") -> List[str]:
    os.makedirs(upload_dir, exist_ok=True)
    saved_paths = []

    for image in images:
        file_path = os.path.join(upload_dir, image.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        saved_paths.append(f"/{file_path}")  # save URL or path
    return saved_paths

def create_product_method(db:Session,product_details:ProductCreate):
    
    image_urls=save_images(images=product_details.image_url)
    product_data = product_details.__dict__.copy()
    product_data.pop("image_url") 
    product=Product(**product_data,image_url=image_urls)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def retrieve_products_method(
    db: Session,
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 10
):
    query = db.query(Product)

    if search:
        query = query.filter(
            or_(
                Product.name.ilike(f"%{search}%"),
                Product.description.ilike(f"%{search}%")
            )
        )

    if category_id is not None:
        query = query.filter(Product.category_id == category_id)

    total = query.count()
    results = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "results": results
    }

def create_category_method(db:Session,category_details:ProductCategoryCreate):

    category=ProductCategory(**category_details.__dict__)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def create_inventory_method(db:Session,inventory_details:ProductInventoryCreate):

    inventory=ProductInventory(**inventory_details.__dict__)
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return inventory

def create_discount_method(db:Session,discount_details:ProductDiscountCreate):

    discount=ProductDiscount(**discount_details.__dict__)
    db.add(discount)
    db.commit()
    db.refresh(discount)
    return discount

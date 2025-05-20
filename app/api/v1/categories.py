from fastapi import APIRouter, Depends, UploadFile,File,HTTPException,Form
from sqlalchemy.orm import Session
from app.db.models import Category
from app.db.schemas import CategoryResponse
from app.db.session import get_db
import tempfile
import cloudinary.uploader
from typing import Optional

router = APIRouter()

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

@router.post("/category",response_model=CategoryResponse)
async def create_category(name:str=Form(...),image_file:UploadFile=File(...),db:Session=Depends(get_db)):
    try:
        upload=await uploadImage(image_file)
        if not upload :
           raise HTTPException(status_code=500,detail="Could not upload image")
        data={
            "name":name,
            "image_url":upload["secure_url"],
            "public_id":upload["public_id"]
        }
        category=Category(**data)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Category creation failed: {str(e)}")

@router.put("/category/{category_id}",response_model=CategoryResponse)
async def update_category(category_id:int,name:Optional[str]=Form(None),image_file:UploadFile=File(...),db:Session=Depends(get_db)):
    try:
        upload=await uploadImage(image_file)
        if not upload :
           raise HTTPException(status_code=500,detail="Could not upload image")
    
        category=db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404,detail="Category not found")
        category.name=name
        category.image_url=upload["secure_url"]
        category.public_id=upload["public_id"]
        db.commit()
        db.refresh(category)
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error updating category:{str(e)}")

@router.get("/get_categories")
async def get_categories(db:Session=Depends(get_db)):
    return db.query(Category).all()
from fastapi import APIRouter, Depends,UploadFile,File,HTTPException
from sqlalchemy.orm import Session
from app.db.models import Variant,VariantImages
from app.db.schemas import VariantCreate, VariantResponse
from app.db.session import get_db
import cloudinary.uploader

router = APIRouter()

@router.post("/", response_model=VariantResponse)
def create_variant(variant: VariantCreate, db: Session = Depends(get_db)):
    db_variant = Variant(**variant.dict())
    db.add(db_variant)
    db.commit()
    db.refresh(db_variant)
    return db_variant

@router.post("/variant_images/{varient_id}")
async def post_variant_images(variant_id:int,files: list[UploadFile] = File(...),db:Session=Depends(get_db)):
    try:
        uploaded_images = []
        for file in files:
            upload_result =cloudinary.uploader.upload(file.file, folder="variants")
            image = VariantImages(variant_id=variant_id, image_url=upload_result["secure_url"])
            db.add(image)
            uploaded_images.append(upload_result["secure_url"])

        db.commit()
        return {"uploaded_variant_images": uploaded_images}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image upload failed: {str(e)}")
    
@router.get("/variants/{variant_id}", response_model=VariantResponse)
async def get_variant(variant_id: int, db: Session = Depends(get_db)):
    variant = db.query(Variant).filter(Variant.id == variant_id).first()

    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")

    images = [img.image_url for img in variant.images]  # ✅ Fetch associated images
    
    return VariantResponse(
        id=variant.id,
        product_id=variant.product_id,
        variant_name=variant.name,
        images=images,
        name=variant.name,
        price=variant.price
    )
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.models import Variant
from app.db.schemas import VariantCreate, VariantResponse
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=VariantResponse)
def create_variant(variant: VariantCreate, db: Session = Depends(get_db)):
    db_variant = Variant(**variant.dict())
    db.add(db_variant)
    db.commit()
    db.refresh(db_variant)
    return db_variant

@router.get("/{variant_id}", response_model=VariantResponse)
def get_variant(variant_id: int, db: Session = Depends(get_db)):
    return db.query(Variant).filter(Variant.id == variant_id).first()

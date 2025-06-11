from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.medication import Medication
from pydantic import BaseModel

router = APIRouter()


class MedicationResponse(BaseModel):
    """Response schema for medication."""
    id: int
    name: str
    active_ingredient: str
    form: str
    unit_type: str
    unit_price: int
    stock: int
    side_effects: str = None
    max_per_day: int = None
    is_supporting: bool
    treatment_class: str
    contraindications: str = None
    allergy_tags: List[str] = []

    class Config:
        from_attributes = True


@router.get("/medications", response_model=List[MedicationResponse])
async def get_medications(
    db: Session = Depends(get_db),
    in_stock_only: bool = True
):
    """
    Returns all available medications in stock.
    
    Args:
        in_stock_only: If True, only return medications with stock > 0
    """
    try:
        query = db.query(Medication)
        
        if in_stock_only:
            query = query.filter(Medication.stock > 0)
        
        medications = query.all()
        
        return medications
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching medications: {str(e)}"
        )


@router.get("/medications/{medication_id}", response_model=MedicationResponse)
async def get_medication(
    medication_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific medication by ID."""
    try:
        medication = db.query(Medication).filter(Medication.id == medication_id).first()
        
        if not medication:
            raise HTTPException(
                status_code=404,
                detail="Medication not found"
            )
        
        return medication
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching medication: {str(e)}"
        )

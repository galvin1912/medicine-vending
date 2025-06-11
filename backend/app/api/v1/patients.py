from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.patient import Patient, Allergy, UnderlyingCondition
from app.schemas.patient import PatientCreate, PatientResponse

router = APIRouter()


@router.get("/patients")
async def get_patients():
    """Get all patients."""
    return {"message": "Patients endpoint - to be implemented"}


@router.post("/patients", response_model=PatientResponse)
async def create_patient(
    patient_data: PatientCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new patient record.
    
    Input: Basic patient info (gender, age, weight, height, allergies, conditions)
    Output: Patient ID and created patient data
    """
    try:
        # Create patient record
        db_patient = Patient(
            gender=patient_data.gender,
            age=patient_data.age,
            weight=patient_data.weight,
            height=patient_data.height
        )
        
        db.add(db_patient)
        db.flush()  # To get the patient ID
        
        # Add allergies if provided
        if patient_data.allergies:
            for allergy_substance in patient_data.allergies:
                allergy = Allergy(
                    patient_id=db_patient.id,
                    substance=allergy_substance
                )
                db.add(allergy)
        
        # Add underlying conditions if provided
        if patient_data.underlying_conditions:
            for condition_name in patient_data.underlying_conditions:
                condition = UnderlyingCondition(
                    patient_id=db_patient.id,
                    condition_name=condition_name
                )
                db.add(condition)
        
        db.commit()
        db.refresh(db_patient)
        
        return db_patient
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error creating patient: {str(e)}"
        )


@router.get("/patients/{patient_id}", response_model=PatientResponse)
async def get_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific patient by ID."""
    try:
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        
        if not patient:
            raise HTTPException(
                status_code=404,
                detail="Patient not found"
            )
        
        return patient
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching patient: {str(e)}"
        )

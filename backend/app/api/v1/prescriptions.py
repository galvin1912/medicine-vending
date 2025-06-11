from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.prescription import Prescription, PrescriptionDose, PrescriptionSupporting
from app.models.medication import Medication
from app.models.patient import Patient
from app.schemas.ai_response import ConfirmPrescriptionResponse, PrescriptionItem
from app.schemas.patient import PatientCreate
from pydantic import BaseModel
from typing import List

router = APIRouter()


class ConfirmPrescriptionRequest(BaseModel):
    """Request schema for confirming prescription."""
    patient_data: PatientCreate
    main_medicines: List[dict]
    supporting_medicines: List[dict]
    doses_per_day: int
    total_days: int
    diagnosis: str = ""
    ai_recommendation: str = ""
    severity_level: str = ""
    side_effects_warning: str = ""
    medical_advice: str = ""
    emergency_status: bool = False
    should_see_doctor: bool = False
    disclaimer: str = ""


@router.post("/prescriptions")
async def create_prescription():
    """Create a new prescription."""
    return {"message": "Create prescription endpoint - to be implemented"}


@router.get("/prescriptions/{prescription_id}")
async def get_prescription(
    prescription_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific prescription by ID."""
    try:
        prescription = db.query(Prescription).filter(
            Prescription.id == prescription_id
        ).first()
        
        if not prescription:
            raise HTTPException(
                status_code=404,
                detail="Prescription not found"
            )
        
        return prescription
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching prescription: {str(e)}"
        )


@router.post("/confirm_prescription", response_model=ConfirmPrescriptionResponse)
async def confirm_prescription(
    request: ConfirmPrescriptionRequest,
    db: Session = Depends(get_db)
):
    """
    Confirm and create a prescription based on AI recommendations.
    
    Input: Patient data, medication recommendations, dosage info
    Output: Prescription ID, total price, detailed breakdown
    """
    try:
        # Create or get patient
        patient = Patient(
            gender=request.patient_data.gender,
            age=request.patient_data.age,
            weight=request.patient_data.weight,
            height=request.patient_data.height
        )
        db.add(patient)
        db.flush()
        
        # Calculate total price and prepare items
        total_price = 0
        prescription_items = []
        
        # Process main medicines
        main_medicine_total_quantities = []
        for med_info in request.main_medicines:
            # First try exact match
            medication = db.query(Medication).filter(
                Medication.name == med_info["name"]
            ).first()
            
            if not medication and "(" in med_info["name"] and ")" in med_info["name"]:
                clean_name = med_info["name"].split("(")[0].strip()
                medication = db.query(Medication).filter(
                    Medication.name == clean_name
                ).first()
            
            if not medication:
                raise HTTPException(
                    status_code=404,
                    detail=f"Medication not found: {med_info['name']}"
                )
            
            # Calculate total quantity needed
            quantity_per_dose = med_info["quantity_per_dose"]
            total_quantity = quantity_per_dose * request.doses_per_day * request.total_days
            
            # Check stock
            if medication.stock < total_quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock for {medication.name}. Available: {medication.stock}, Required: {total_quantity}"
                )
            
            item_price = total_quantity * medication.unit_price
            total_price += item_price
            
            prescription_items.append(PrescriptionItem(
                name=medication.name,
                total_quantity=total_quantity,
                price=item_price
            ))
            
            main_medicine_total_quantities.append({
                "medication": medication,
                "quantity_per_dose": quantity_per_dose,
                "total_quantity": total_quantity
            })
        
        # Process supporting medicines
        supporting_medicine_data = []
        for med_info in request.supporting_medicines:
            # First try exact match
            medication = db.query(Medication).filter(
                Medication.name == med_info["name"]
            ).first()
            
            # If not found, try to extract medication name (remove active ingredient part)
            if not medication and "(" in med_info["name"] and ")" in med_info["name"]:
                clean_name = med_info["name"].split("(")[0].strip()
                medication = db.query(Medication).filter(
                    Medication.name == clean_name
                ).first()
            
            if not medication:
                raise HTTPException(
                    status_code=404,
                    detail=f"Supporting medication not found: {med_info['name']}"
                )
            
            total_quantity = med_info.get("quantity_total", med_info.get("quantity_per_day", 1))
            
            # Check stock
            if medication.stock < total_quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock for {medication.name}. Available: {medication.stock}, Required: {total_quantity}"
                )
            
            item_price = total_quantity * medication.unit_price
            total_price += item_price
            
            prescription_items.append(PrescriptionItem(
                name=medication.name,
                total_quantity=total_quantity,
                price=item_price
            ))
            
            supporting_medicine_data.append({
                "medication": medication,
                "total_quantity": total_quantity
            })
        
        # Create prescription record
        prescription = Prescription(
            patient_id=patient.id,
            doses_per_day=request.doses_per_day,
            days=request.total_days,
            total_price=total_price,
            diagnosis=request.diagnosis,
            ai_recommendation=request.ai_recommendation
        )
        db.add(prescription)
        db.flush()
        
        # Create prescription dose records (main medicines)
        for med_data in main_medicine_total_quantities:
            dose_record = PrescriptionDose(
                prescription_id=prescription.id,
                medication_id=med_data["medication"].id,
                quantity_per_dose=med_data["quantity_per_dose"],
                dose_time="regular"  # Could be enhanced with specific times
            )
            db.add(dose_record)
        
        # Create prescription supporting records
        for med_data in supporting_medicine_data:
            supporting_record = PrescriptionSupporting(
                prescription_id=prescription.id,
                medication_id=med_data["medication"].id,
                quantity_total=med_data["total_quantity"]
            )
            db.add(supporting_record)
        
        # Update medication stock
        for med_data in main_medicine_total_quantities:
            med_data["medication"].stock -= med_data["total_quantity"]
        
        for med_data in supporting_medicine_data:
            med_data["medication"].stock -= med_data["total_quantity"]
        
        db.commit()
        
        # Prepare response
        response = ConfirmPrescriptionResponse(
            prescription_id=prescription.id,
            total_price=total_price,
            diagnosis=request.diagnosis or "Chẩn đoán dựa trên triệu chứng được phân tích.",
            usage_instructions=f"Uống thuốc {request.doses_per_day} lần mỗi ngày trong {request.total_days} ngày. Uống sau ăn và uống nhiều nước.",
            side_effects_warning=request.side_effects_warning,
            medical_advice=request.medical_advice,
            recommendation_reasoning=request.ai_recommendation or "Thuốc được lựa chọn dựa trên phân tích triệu chứng và thông tin bệnh nhân.",
            severity_level=request.severity_level,
            emergency_status=request.emergency_status,
            should_see_doctor=request.should_see_doctor,
            disclaimer=request.disclaimer,
            items=prescription_items
        )
        
        return response
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error confirming prescription: {str(e)}"
        )

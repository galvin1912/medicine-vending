from pydantic import BaseModel
from typing import List, Optional


class MedicineRecommendation(BaseModel):
    """Single medicine recommendation."""
    name: str
    quantity_per_dose: int
    reason: str


class SupportingMedicine(BaseModel):
    """Supporting medicine recommendation."""
    name: str
    quantity_per_day: Optional[int] = None
    quantity: Optional[int] = None  # For items like face masks
    reason: str


class PatientAnalysisRequest(BaseModel):
    """Request schema for patient analysis."""
    symptoms: str
    gender: str
    age: int
    height: int
    weight: int
    allergies: List[str] = []
    underlying_conditions: List[str] = []
    current_medications: List[str] = []


class AIAnalysisResponse(BaseModel):
    """AI analysis response schema as per PRD."""
    main_medicines: List[MedicineRecommendation]
    supporting_medicines: List[SupportingMedicine]
    doses_per_day: int
    total_days: int
    recommendation_reasoning: str
    diagnosis: str
    severity_level: str
    side_effects_warning: str
    medical_advice: str
    emergency_status: bool
    should_see_doctor: bool
    disclaimer: str


class PrescriptionItem(BaseModel):
    """Single prescription item."""
    name: str
    total_quantity: int
    price: int  # in VND


class ConfirmPrescriptionResponse(BaseModel):
    """Prescription confirmation response schema as per PRD."""
    prescription_id: int
    total_price: int  # in VND
    diagnosis: str
    usage_instructions: str
    side_effects_warning: str
    medical_advice: str
    recommendation_reasoning: str
    severity_level: str
    emergency_status: bool
    should_see_doctor: bool
    disclaimer: str
    items: List[PrescriptionItem]

from pydantic import BaseModel
from typing import List, Optional


class AllergyBase(BaseModel):
    """Base allergy schema."""
    substance: str


class AllergyResponse(AllergyBase):
    """Allergy response schema."""
    id: int
    patient_id: int

    class Config:
        from_attributes = True


class UnderlyingConditionBase(BaseModel):
    """Base underlying condition schema."""
    condition_name: str


class UnderlyingConditionResponse(UnderlyingConditionBase):
    """Underlying condition response schema."""
    id: int
    patient_id: int

    class Config:
        from_attributes = True


class PatientBase(BaseModel):
    """Base patient schema."""
    gender: str
    age: int
    weight: int  # in kg
    height: int  # in cm


class PatientCreate(PatientBase):
    """Patient creation schema."""
    allergies: List[str] = []
    underlying_conditions: List[str] = []


class PatientResponse(PatientBase):
    """Patient response schema."""
    id: int
    allergies: List[AllergyResponse] = []
    underlying_conditions: List[UnderlyingConditionResponse] = []

    class Config:
        from_attributes = True

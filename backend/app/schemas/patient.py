from pydantic import BaseModel
from typing import List, Optional


class PatientBase(BaseModel):
    """Base patient schema."""
    gender: str
    age: int
    weight: int
    height: int


class PatientCreate(PatientBase):
    """Schema for creating a patient."""
    allergies: List[str] = []
    underlying_conditions: List[str] = []


class Patient(PatientBase):
    """Patient response schema."""
    id: int
    allergies: List[str] = []
    underlying_conditions: List[str] = []

    class Config:
        from_attributes = True

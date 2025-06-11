# Import Base from connection module
from app.database.connection import Base

# Import all models here for Alembic to detect them
# This ensures that all models are available when creating migrations
from app.models.patient import Patient
from app.models.medication import Medication, Symptom
from app.models.prescription import Prescription, PrescriptionDose, PrescriptionSupporting

__all__ = [
    "Base",
    "Patient", 
    "Medication",
    "Symptom",
    "Prescription",
    "PrescriptionDose", 
    "PrescriptionSupporting"
]

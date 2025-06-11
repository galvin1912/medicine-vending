from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.connection import Base


class Prescription(Base):
    """Prescription model."""
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    doses_per_day = Column(Integer, nullable=False)
    days = Column(Integer, nullable=False)
    total_price = Column(Integer, nullable=False)  # Total price in VND

    # Relationships
    patient = relationship("Patient", back_populates="prescriptions")
    doses = relationship("PrescriptionDose", back_populates="prescription", cascade="all, delete-orphan")
    supportings = relationship("PrescriptionSupporting", back_populates="prescription", cascade="all, delete-orphan")
    usage_logs = relationship("UsageLog", back_populates="prescription", cascade="all, delete-orphan")


class PrescriptionDose(Base):
    """Prescription doses model - main medicines taken per dose."""
    __tablename__ = "prescription_doses"

    id = Column(Integer, primary_key=True, index=True)
    prescription_id = Column(Integer, ForeignKey("prescriptions.id"), nullable=False)
    medication_id = Column(Integer, ForeignKey("medications.id"), nullable=False)
    quantity_per_dose = Column(Integer, nullable=False)

    # Relationships
    prescription = relationship("Prescription", back_populates="doses")
    medication = relationship("Medication", back_populates="prescription_doses")


class PrescriptionSupporting(Base):
    """Prescription supporting medicines model - supporting items."""
    __tablename__ = "prescription_supportings"

    id = Column(Integer, primary_key=True, index=True)
    prescription_id = Column(Integer, ForeignKey("prescriptions.id"), nullable=False)
    medication_id = Column(Integer, ForeignKey("medications.id"), nullable=False)
    quantity_total = Column(Integer, nullable=False)

    # Relationships
    prescription = relationship("Prescription", back_populates="supportings")
    medication = relationship("Medication", back_populates="prescription_supportings")


class UsageLog(Base):
    """Usage logs model."""
    __tablename__ = "usage_logs"

    id = Column(Integer, primary_key=True, index=True)
    prescription_id = Column(Integer, ForeignKey("prescriptions.id"), nullable=False)
    note = Column(Text)
    generated_by = Column(Text)

    # Relationships
    prescription = relationship("Prescription", back_populates="usage_logs")

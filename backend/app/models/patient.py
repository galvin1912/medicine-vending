from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database.connection import Base


class Patient(Base):
    """Patient model."""
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    gender = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)  # in kg
    height = Column(Integer, nullable=False)  # in cm

    # Relationships
    allergies = relationship("Allergy", back_populates="patient", cascade="all, delete-orphan")
    underlying_conditions = relationship("UnderlyingCondition", back_populates="patient", cascade="all, delete-orphan")
    prescriptions = relationship("Prescription", back_populates="patient")


class Allergy(Base):
    """Patient allergies model."""
    __tablename__ = "allergies"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    substance = Column(Text, nullable=False)

    # Relationships
    patient = relationship("Patient", back_populates="allergies")


class UnderlyingCondition(Base):
    """Patient underlying conditions model."""
    __tablename__ = "underlying_conditions"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    condition_name = Column(Text, nullable=False)

    # Relationships
    patient = relationship("Patient", back_populates="underlying_conditions")

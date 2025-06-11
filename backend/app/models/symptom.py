"""
Symptom model for storing medical symptoms.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database.connection import Base

# Association table for many-to-many relationship between medications and symptoms
medication_symptom = Table(
    'medication_symptom',
    Base.metadata,
    Column('medication_id', Integer, ForeignKey('medications.id'), primary_key=True),
    Column('symptom_id', Integer, ForeignKey('symptoms.id'), primary_key=True)
)


class Symptom(Base):
    """Symptom model as per PRD specification."""
    __tablename__ = "symptoms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    # Many-to-many relationship with medications
    medications = relationship(
        "Medication", 
        secondary=medication_symptom, 
        back_populates="symptoms"
    )

    def __repr__(self):
        return f"<Symptom(id={self.id}, name='{self.name}')>" 
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from app.database.connection import Base


class Medication(Base):
    """Medication model."""
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)  # Tên thương mại
    active_ingredient = Column(Text, nullable=False)  # Hoạt chất chính
    form = Column(Text, nullable=False)  # Dạng bào chế (viên, siro, gói...)
    unit_type = Column(Text, nullable=False)  # Đơn vị tính (viên, gói, chai...)
    unit_price = Column(Integer, nullable=False)  # Giá cho mỗi đơn vị (đồng)
    stock = Column(Integer, nullable=False, default=0)  # Số lượng còn trong kho
    side_effects = Column(Text)  # Tác dụng phụ phổ biến
    max_per_day = Column(Integer)  # Liều tối đa/ngày
    is_supporting = Column(Boolean, default=False)  # Có phải thuốc hỗ trợ hay không
    treatment_class = Column(Text)  # Nhóm điều trị
    contraindications = Column(Text)  # Chống chỉ định
    allergy_tags = Column(ARRAY(Text))  # Các thành phần có thể gây dị ứng

    symptoms = relationship(
        "Symptom", 
        secondary="medication_symptom", 
        back_populates="medications"
    )
    
    prescription_doses = relationship("PrescriptionDose", back_populates="medication")
    prescription_supportings = relationship("PrescriptionSupporting", back_populates="medication")

    def __repr__(self):
        return f"<Medication(id={self.id}, name='{self.name}', stock={self.stock})>"

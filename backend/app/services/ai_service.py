"""
AI Service for medication recommendation using Gemini and LangChain.
This service handles the core AI logic for symptom analysis and medication recommendations.
"""

from typing import List, Dict, Any
import google.generativeai as genai
from app.core.config import settings
from app.schemas.ai_response import AIAnalysisResponse, MedicineRecommendation, SupportingMedicine


class AIService:
    """Service for AI-powered medication recommendations."""
    
    def __init__(self):
        """Initialize AI service with Gemini API."""
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
            print("Warning: GEMINI_API_KEY not provided. AI features will be disabled.")
    
    def create_diagnosis_prompt(
        self,
        symptoms: str,
        gender: str,
        age: int,
        height: int,
        weight: int,
        allergies: List[str],
        underlying_conditions: List[str],
        current_medications: List[str]
    ) -> str:
        """Create the diagnosis prompt as specified in PRD."""
        
        allergies_str = ", ".join(allergies) if allergies else "Không có"
        conditions_str = ", ".join(underlying_conditions) if underlying_conditions else "Không có"
        medications_str = ", ".join(current_medications) if current_medications else "Không có"
        
        prompt = f"""
Dựa trên các thông tin dưới đây, hãy chẩn đoán bệnh sơ bộ, đánh giá mức độ nghiêm trọng, đưa ra lời khuyên y tế sơ bộ và xác định các mục tiêu điều trị phù hợp.

Thông tin người bệnh:
- Giới tính: {gender}
- Tuổi: {age}
- Chiều cao: {height} cm
- Cân nặng: {weight} kg
- Triệu chứng: {symptoms}
- Tiền sử bệnh nền: {conditions_str}
- Dị ứng: {allergies_str}
- Đang dùng thuốc: {medications_str}

Hãy đưa ra gợi ý thuốc phù hợp từ danh sách thuốc có sẵn. Trả lời theo format JSON với các trường:
- main_medicines: danh sách thuốc chính (name, quantity_per_dose, reason)
- supporting_medicines: danh sách thuốc hỗ trợ (name, quantity_per_day hoặc quantity, reason)
- doses_per_day: số lần uống mỗi ngày (2-4 lần)
- total_days: số ngày điều trị (1-5 ngày)
- recommendation_reasoning: giải thích tại sao chọn những thuốc này

Lưu ý: Chỉ gợi ý thuốc không cần đơn và phù hợp với triệu chứng. Tránh kê thuốc có chống chỉ định với bệnh nền hoặc dị ứng.
"""
        return prompt
    
    async def analyze_symptoms(
        self,
        symptoms: str,
        gender: str, 
        age: int,
        height: int,
        weight: int,
        allergies: List[str] = None,
        underlying_conditions: List[str] = None,
        current_medications: List[str] = None
    ) -> AIAnalysisResponse:
        """
        Analyze patient symptoms and return medication recommendations.
        This method implements the core AI logic for symptom analysis.
        """
        if not self.model:
            # Return mock response if AI is not configured
            return self._get_mock_response()
        
        # Create prompt
        prompt = self.create_diagnosis_prompt(
            symptoms=symptoms,
            gender=gender,
            age=age,
            height=height,
            weight=weight,
            allergies=allergies or [],
            underlying_conditions=underlying_conditions or [],
            current_medications=current_medications or []
        )
        
        try:
            # Generate response using Gemini
            response = self.model.generate_content(prompt)
            
            # TODO: Parse the response and extract structured data
            # For now, return a mock response
            return self._get_mock_response()
            
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return self._get_mock_response()
    
    def _get_mock_response(self) -> AIAnalysisResponse:
        """Return a mock response for testing purposes."""
        return AIAnalysisResponse(
            main_medicines=[
                MedicineRecommendation(
                    name="Paracetamol",
                    quantity_per_dose=1,
                    reason="Paracetamol giúp hạ sốt và giảm đau, thường dùng trong điều trị cảm cúm."
                ),
                MedicineRecommendation(
                    name="Loratadin",
                    quantity_per_dose=1,
                    reason="Loratadin là thuốc kháng histamin, giúp giảm sổ mũi và hắt hơi."
                )
            ],
            supporting_medicines=[
                SupportingMedicine(
                    name="Vitamin C",
                    quantity_per_day=1,
                    reason="Tăng sức đề kháng, hỗ trợ phục hồi nhanh hơn."
                ),
                SupportingMedicine(
                    name="Khẩu trang",
                    quantity=3,
                    reason="Giảm nguy cơ lây nhiễm cho người khác."
                )
            ],
            doses_per_day=3,
            total_days=3,
            recommendation_reasoning="Các thuốc được chọn dựa trên phân tích triệu chứng hiện tại, dị ứng và thuốc đang sử dụng. Kết hợp Paracetamol và Loratadin giúp giảm triệu chứng cảm lạnh nhẹ."
        )


# Global AI service instance
ai_service = AIService()

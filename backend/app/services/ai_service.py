"""
AI Service for medication recommendation using Gemini and LangChain.
This service handles the core AI logic for symptom analysis and medication recommendations.
"""

from typing import List, Dict, Any
from app.core.config import settings
from app.schemas.ai_response import AIAnalysisResponse, MedicineRecommendation, SupportingMedicine

# LangChain imports
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableSequence
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

# Vector store imports
from app.services.vector_store_manager import vector_store_manager


class AIRecommendationOutput(BaseModel):
    """Pydantic model for structured AI output parsing."""
    main_medicines: List[Dict[str, Any]] = Field(
        description="List of main medicine recommendations with name, quantity_per_dose, and reason fields"
    )
    supporting_medicines: List[Dict[str, Any]] = Field(
        description="List of supporting medicine recommendations with name, quantity_per_day (or quantity), and reason fields"
    )
    doses_per_day: int = Field(description="Number of doses per day", ge=1, le=4)
    total_days: int = Field(description="Total days of treatment", ge=1, le=5)
    recommendation_reasoning: str = Field(description="Detailed reasoning for the recommendation")


class AIService:
    """Service for AI-powered medication recommendations using LangChain."""
    
    def __init__(self):
        """Initialize AI service with LangChain and Gemini."""
        if settings.gemini_api_key:
            # Initialize LangChain components
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                google_api_key=settings.gemini_api_key,
                temperature=0.1
            )
            
            # Initialize output parser
            self.output_parser = PydanticOutputParser(pydantic_object=AIRecommendationOutput)
            
            # Initialize prompt template
            self.prompt_template = PromptTemplate(
                template=self._get_prompt_template(),
                input_variables=[
                    "gender", "age", "height", "weight", "symptoms", 
                    "underlying_conditions", "allergies", "current_medications", 
                    "med_context", "format_instructions"
                ]
            )
            
            # Create the processing chain
            self.chain = RunnableSequence(
                self.prompt_template,
                self.llm,
                self.output_parser
            )
            
        else:
            self.llm = None
            self.chain = None
            print("Warning: GEMINI_API_KEY not provided. AI features will be disabled.")
    
    def _get_prompt_template(self) -> str:
        """Get the prompt template as specified in PRD."""
        return """Dựa trên các thông tin dưới đây, hãy chẩn đoán bệnh sơ bộ, đánh giá mức độ nghiêm trọng, đưa ra lời khuyên y tế sơ bộ và xác định các mục tiêu điều trị phù hợp.

        Thông tin người bệnh:
        - Giới tính: {gender}
        - Tuổi: {age}
        - Chiều cao: {height} cm
        - Cân nặng: {weight} kg
        - Triệu chứng: {symptoms}
        - Tiền sử bệnh nền: {underlying_conditions}
        - Dị ứng: {allergies}
        - Đang dùng thuốc: {current_medications}{med_context}

        Hãy phân tích triệu chứng và đưa ra gợi ý thuốc phù hợp. CHỈ gợi ý thuốc có trong danh sách trên và phù hợp với triệu chứng.

        Lưu ý quan trọng:
        - CHỈ chọn thuốc từ danh sách có sẵn
        - Tránh thuốc có chống chỉ định với bệnh nền hoặc dị ứng
        - Không kê thuốc kháng sinh trừ khi thực sự cần thiết
        - Ưu tiên thuốc an toàn, không cần đơn
        - Số lần uống: 2-4 lần/ngày
        - Số ngày điều trị: 1-5 ngày cho triệu chứng nhẹ

        Trả lời theo CHÍNH XÁC định dạng JSON sau với các field bắt buộc:
        - main_medicines: array của các object với fields "name" (string), "quantity_per_dose" (integer, CHỈ SỐ không có đơn vị), "reason" (string)
        - supporting_medicines: array của các object với fields "name" (string), "quantity_per_day" (integer, CHỈ SỐ không có đơn vị), "reason" (string)
        - doses_per_day: integer từ 1-4
        - total_days: integer từ 1-5
        - recommendation_reasoning: string giải thích chi tiết

        QUAN TRỌNG: Tất cả quantity_per_dose và quantity_per_day phải là số nguyên (ví dụ: 1, 2, 3) KHÔNG phải chuỗi có đơn vị (ví dụ: "1 viên", "2 gói").

        {format_instructions}"""

    def create_diagnosis_prompt_data(
        self,
        symptoms: str,
        gender: str,
        age: int,
        height: int,
        weight: int,
        allergies: List[str],
        underlying_conditions: List[str],
        current_medications: List[str]
    ) -> Dict[str, str]:
        """Create prompt data for LangChain template."""
        
        allergies_str = ", ".join(allergies) if allergies else "Không có"
        conditions_str = ", ".join(underlying_conditions) if underlying_conditions else "Không có"
        medications_str = ", ".join(current_medications) if current_medications else "Không có"
        
        # Get vector store context for enhanced recommendations
        vector_context = vector_store_manager.get_vector_context_for_prompt(
            symptoms=symptoms,
            allergies=allergies
        )
        
        return {
            "gender": gender,
            "age": str(age),
            "height": str(height),
            "weight": str(weight),
            "symptoms": symptoms,
            "underlying_conditions": conditions_str,
            "allergies": allergies_str,
            "current_medications": medications_str,
            "med_context": vector_context,
            "format_instructions": self.output_parser.get_format_instructions()
        }

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
        Analyze patient symptoms and return medication recommendations using LangChain.
        This method implements the core AI logic for symptom analysis.
        """
        if not self.chain:
            # Return mock response if AI is not configured
            return self._get_mock_response(symptoms)
        
        try:
            # Prepare prompt data
            prompt_data = self.create_diagnosis_prompt_data(
                symptoms=symptoms,
                gender=gender,
                age=age,
                height=height,
                weight=weight,
                allergies=allergies or [],
                underlying_conditions=underlying_conditions or [],
                current_medications=current_medications or []
            )
            
            # Execute LangChain pipeline
            result = await self.chain.ainvoke(prompt_data)
            
            # Convert to our response format
            main_medicines = [
                MedicineRecommendation(**med) 
                for med in result.main_medicines
            ]
            
            supporting_medicines = [
                SupportingMedicine(**med) 
                for med in result.supporting_medicines
            ]
            
            return AIAnalysisResponse(
                main_medicines=main_medicines,
                supporting_medicines=supporting_medicines,
                doses_per_day=result.doses_per_day,
                total_days=result.total_days,
                recommendation_reasoning=result.recommendation_reasoning
            )
            
        except Exception as e:
            print(f"Error in LangChain pipeline: {e}")
            # Fallback to mock response if LangChain fails
            return self._get_mock_response(symptoms)
    
    def _get_mock_response(self, symptoms: str = "") -> AIAnalysisResponse:
        """Return a fallback response when AI is not working."""
        return AIAnalysisResponse(
            main_medicines=[],
            supporting_medicines=[],
            doses_per_day=0,
            total_days=0,
            recommendation_reasoning="AI hiện không hoạt động. Vui lòng đến bệnh viện để được khám và tư vấn trực tiếp từ bác sĩ."
        )


# Global AI service instance
ai_service = AIService()

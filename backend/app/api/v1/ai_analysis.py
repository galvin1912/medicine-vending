from fastapi import APIRouter, HTTPException
from app.schemas.ai_response import PatientAnalysisRequest, AIAnalysisResponse
from app.services.ai_service import ai_service

router = APIRouter()


@router.post("/analyze_input", response_model=AIAnalysisResponse)
async def analyze_patient_input(
    request: PatientAnalysisRequest,
):
    """
    Analyze patient symptoms and information using AI.
    This endpoint processes patient data and returns medication recommendations.
    """
    try:
        response = await ai_service.analyze_symptoms(
            symptoms=request.symptoms,
            gender=request.gender,
            age=request.age,
            height=request.height,
            weight=request.weight,
            allergies=request.allergies,
            underlying_conditions=request.underlying_conditions,
            current_medications=request.current_medications
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing patient input: {str(e)}"
        )
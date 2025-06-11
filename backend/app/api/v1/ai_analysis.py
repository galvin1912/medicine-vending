from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.ai_response import PatientAnalysisRequest, AIAnalysisResponse
from app.services.ai_service import ai_service

router = APIRouter()


@router.post("/analyze_input", response_model=AIAnalysisResponse)
async def analyze_patient_input(
    request: PatientAnalysisRequest,
    db: Session = Depends(get_db)
):
    """
    Analyze patient symptoms and information using AI.
    This endpoint processes patient data and returns medication recommendations.
    """
    try:
        # Call AI service to analyze symptoms
        # Vector store will handle medication selection intelligently
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


@router.post("/diagnosis")
async def get_diagnosis(
    request: PatientAnalysisRequest,
    db: Session = Depends(get_db)
):
    """Get AI-powered diagnosis based on symptoms."""
    try:
        # Vector store handles medication selection intelligently
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
        
        return {
            "diagnosis": response.recommendation_reasoning,
            "severity": "mild",  # Could be enhanced with severity analysis
            "recommendations": response.main_medicines
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting diagnosis: {str(e)}"
        )

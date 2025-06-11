"""
Vector Store API endpoints for managing medical knowledge embeddings.
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.vector_store_manager import vector_store_manager
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter()


class VectorStoreResponse(BaseModel):
    """Response schema for vector store operations."""
    success: bool
    message: str
    stats: Dict[str, Any] = {}


class MedicationSearchRequest(BaseModel):
    """Request schema for medication search."""
    symptoms: str
    allergies: List[str] = []
    k: int = 10


class MedicationSearchResponse(BaseModel):
    """Response schema for medication search."""
    medications: List[Dict[str, Any]]
    total_found: int


@router.get("/status", response_model=VectorStoreResponse)
async def get_vector_store_status():
    """Get current status of vector stores."""
    try:
        stats = vector_store_manager.get_store_stats()
        
        return VectorStoreResponse(
            success=True,
            message="Vector store status retrieved successfully",
            stats=stats
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting vector store status: {str(e)}"
        )


@router.post("/initialize", response_model=VectorStoreResponse)
async def initialize_vector_stores(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Initialize vector stores from database."""
    try:
        # Initialize in background to avoid timeout
        background_tasks.add_task(vector_store_manager.initialize, db)
        
        return VectorStoreResponse(
            success=True,
            message="Vector store initialization started in background",
            stats=vector_store_manager.get_store_stats()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error initializing vector stores: {str(e)}"
        )


@router.post("/rebuild", response_model=VectorStoreResponse)
async def rebuild_vector_stores(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Rebuild vector stores from current database data."""
    try:
        # Rebuild in background to avoid timeout
        background_tasks.add_task(vector_store_manager.rebuild_stores, db)
        
        return VectorStoreResponse(
            success=True,
            message="Vector store rebuild started in background",
            stats=vector_store_manager.get_store_stats()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error rebuilding vector stores: {str(e)}"
        )


@router.post("/search/medications", response_model=MedicationSearchResponse)
async def search_medications(request: MedicationSearchRequest):
    """Search for relevant medications using vector similarity."""
    try:
        if not vector_store_manager.is_initialized():
            raise HTTPException(
                status_code=503,
                detail="Vector stores not initialized. Please initialize first."
            )
        
        medications = vector_store_manager.get_medication_recommendations(
            symptoms=request.symptoms,
            allergies=request.allergies,
            k=request.k
        )
        
        return MedicationSearchResponse(
            medications=medications,
            total_found=len(medications)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching medications: {str(e)}"
        )


@router.get("/search/test")
async def test_vector_search():
    """Test endpoint for vector search functionality."""
    try:
        if not vector_store_manager.is_initialized():
            return {
                "initialized": False,
                "message": "Vector stores not initialized"
            }
        
        # Test search with common symptoms
        test_symptoms = "đau đầu, sổ mũi"
        recommendations = vector_store_manager.get_medication_recommendations(
            symptoms=test_symptoms,
            k=5
        )
        
        return {
            "initialized": True,
            "test_symptoms": test_symptoms,
            "recommendations_found": len(recommendations),
            "sample_recommendations": recommendations[:3] if recommendations else []
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in test search: {str(e)}"
        ) 
from fastapi import APIRouter

router = APIRouter()


@router.get("/medications")
async def get_medications():
    """Get all available medications."""
    return {"message": "Medications endpoint - to be implemented"}


@router.get("/medications/{medication_id}")
async def get_medication(medication_id: int):
    """Get specific medication by ID."""
    return {"message": f"Get medication {medication_id} - to be implemented"}

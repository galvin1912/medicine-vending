from fastapi import APIRouter

router = APIRouter()


@router.get("/patients")
async def get_patients():
    """Get all patients."""
    return {"message": "Patients endpoint - to be implemented"}


@router.post("/patients")
async def create_patient():
    """Create a new patient."""
    return {"message": "Create patient endpoint - to be implemented"}

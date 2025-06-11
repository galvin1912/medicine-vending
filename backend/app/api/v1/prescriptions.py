from fastapi import APIRouter

router = APIRouter()


@router.post("/prescriptions")
async def create_prescription():
    """Create a new prescription."""
    return {"message": "Create prescription endpoint - to be implemented"}


@router.get("/prescriptions/{prescription_id}")
async def get_prescription(prescription_id: int):
    """Get prescription by ID."""
    return {"message": f"Get prescription {prescription_id} - to be implemented"}


@router.post("/confirm_prescription")
async def confirm_prescription():
    """Confirm and finalize prescription."""
    return {"message": "Confirm prescription endpoint - to be implemented"}

from fastapi import APIRouter, HTTPException
from services.disease_service import get_disease_by_name, populate_sample_diseases

router = APIRouter()

@router.get("/disease/{disease_name}")
async def get_disease_details(disease_name: str):
    """Get detailed information about a specific disease"""
    try:
        disease_info = get_disease_by_name(disease_name)
        return {
            "success": True,
            "disease": disease_info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/populate-diseases")
async def populate_diseases():
    """Populate sample disease data"""
    try:
        populate_sample_diseases()
        return {
            "success": True,
            "message": "Sample diseases populated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

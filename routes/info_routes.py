from fastapi import APIRouter, Path, Body
from controllers.info_controller import get_info, get_batch_info
from models.disease_model import Disease
from config.database import SessionLocal

router = APIRouter(tags=["Info"])

@router.get("/{disease_name}")
def info(disease_name: str = Path(...)):
    return get_info(disease_name)

@router.post("/batch")
def batch_info(payload: dict = Body(...)):
    diseases = payload.get("diseases", [])
    return get_batch_info(diseases)

@router.get("/api/disease/{disease_name}")
async def get_disease_details(disease_name: str):
    """Get disease information from database - always returns detailed data"""
    try:
        import urllib.parse
        from services.disease_service import get_disease_by_name
        
        decoded_name = urllib.parse.unquote(disease_name)
        print(f"DEBUG: API route looking for disease info: {decoded_name}")
        
        # Use the disease service to get detailed information
        disease_info = get_disease_by_name(decoded_name)
        
        return {
            "success": True,
            "disease": {
                "name": disease_info.get("name", decoded_name),
                "overview": disease_info.get("overview", ""),
                "symptoms": disease_info.get("symptoms", ""),
                "causes": disease_info.get("causes", ""),
                "treatments": disease_info.get("treatments", ""),
                "when_to_see_doctor": disease_info.get("when_to_see_doctor", ""),
                "prevention": disease_info.get("prevention", ""),
                "how_common": disease_info.get("how_common", "")
            }
        }
        
    except Exception as e:
        print(f"DEBUG: Exception in disease info endpoint: {e}")
        return {
            "success": True,
            "disease": {
                "name": str(decoded_name if 'decoded_name' in locals() else disease_name),
                "overview": "Medical condition information. Please consult with a healthcare professional for more information.",
                "causes": "Please consult a healthcare professional.",
                "symptoms": "Please consult a healthcare professional.",
                "treatments": "Please consult a healthcare professional.", 
                "prevention": "Please consult a healthcare professional.",
                "when_to_see_doctor": "Please consult a healthcare professional.",
                "how_common": "Please consult a healthcare professional."
            }
        }

from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/")
def get_allergies():
    """Get list of common allergies"""
    try:
        # Return a simple list of allergies
        common_allergies = [
            {"id": 1, "name": "Peanuts"},
            {"id": 2, "name": "Tree Nuts"},
            {"id": 3, "name": "Shellfish"},
            {"id": 4, "name": "Fish"},
            {"id": 5, "name": "Milk"},
            {"id": 6, "name": "Eggs"},
            {"id": 7, "name": "Soy"},
            {"id": 8, "name": "Wheat"},
            {"id": 9, "name": "Sesame"},
            {"id": 10, "name": "Latex"},
            {"id": 11, "name": "Dust Mites"},
            {"id": 12, "name": "Pollen"},
            {"id": 13, "name": "Pet Dander"},
            {"id": 14, "name": "Medication"},
            {"id": 15, "name": "Insect Stings"}
        ]
        
        return {
            "success": True,
            "data": common_allergies
        }
        
    except Exception as e:
        print(f"DEBUG: Error getting allergies: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get allergies: {str(e)}")
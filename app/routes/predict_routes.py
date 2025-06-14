from fastapi import APIRouter, HTTPException
from services.predict_service import test_all_medical_patterns, quick_test_symptoms

router = APIRouter()

@router.get("/test-medical-logic")
async def test_medical_logic():
    """Test all medical logic patterns"""
    try:
        results = test_all_medical_patterns()
        return {
            "success": True,
            "test_results": results,
            "message": f"Tests completed: {results['passed']}/{results['total']} passed"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test failed: {str(e)}")

@router.post("/test-symptoms")
async def test_specific_symptoms(request: dict):
    """Test specific symptom combinations"""
    try:
        symptoms = request.get("symptoms", [])
        if not symptoms:
            raise HTTPException(status_code=400, detail="No symptoms provided")
        
        results = quick_test_symptoms(symptoms)
        return {
            "success": True,
            "symptoms": symptoms,
            "predictions": results[:3]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test failed: {str(e)}")
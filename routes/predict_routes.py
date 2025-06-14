from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from controllers.predict_controller import handle_get_predictions, handle_delete_prediction
from services.predict_service import predict_result, test_all_medical_patterns, quick_test_symptoms, get_predictions_by_user

router = APIRouter()

class PredictRequest(BaseModel):
    symptoms: List[str]
    duration: str = "1-3 days"
    severity: str = "Mild"
    user_id: int

class TestSymptomsRequest(BaseModel):
    symptoms: List[str]

# MAIN PREDICTION ENDPOINT - Fix the route
@router.post("")
async def predict_endpoint(request: PredictRequest):
    """Main prediction endpoint - ML-driven with enhanced medical logic"""
    try:
        data = request.dict()
        result = predict_result(data)
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.post("/")
async def predict_with_slash(request: PredictRequest):
    """Same endpoint with trailing slash"""
    return await predict_endpoint(request)

@router.post("/predict")
async def predict_no_slash(request: PredictRequest):
    """Same endpoint without slash"""
    return await predict_endpoint(request)

@router.post("/predict/") 
async def predict_with_slash(request: PredictRequest):
    """Same endpoint with trailing slash"""
    return await predict_endpoint(request)

@router.get("/{user_id}")
async def get_user_predictions(user_id: int):
    """Get user's prediction history"""
    try:
        result = handle_get_predictions(user_id)
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=404, detail=result["message"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get predictions: {str(e)}")

@router.delete("/{predict_id}")
async def delete_prediction(predict_id: int):
    """Delete a specific prediction"""
    try:
        print(f"DEBUG: Attempting to delete prediction {predict_id}")
        result = handle_delete_prediction(predict_id)
        print(f"DEBUG: Delete result: {result}")
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=404, detail=result["message"])
    except Exception as e:
        print(f"DEBUG: Delete prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete prediction: {str(e)}")

@router.get("/test-logic")
async def test_medical_logic():
    """Test all medical logic patterns for debugging"""
    try:
        results = test_all_medical_patterns()
        return {
            "success": True,
            "test_results": results,
            "message": f"Tests completed: {results['passed']}/{results['total']} passed ({results['passed']/results['total']*100:.1f}%)"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test failed: {str(e)}")

@router.post("/test-symptoms")
async def test_specific_symptoms(request: TestSymptomsRequest):
    """Test specific symptom combinations for debugging"""
    try:
        symptoms = request.symptoms
        if not symptoms:
            raise HTTPException(status_code=400, detail="No symptoms provided")
        
        results = quick_test_symptoms(symptoms)
        return {
            "success": True,
            "symptoms": symptoms,
            "predictions": results[:5],
            "top_3": results[:3]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test failed: {str(e)}")

@router.get("/symptoms")
async def get_available_symptoms():
    """Get list of all available symptoms"""
    from services.predict_service import symptom_columns
    
    return {
        "success": True,
        "total_symptoms": len(symptom_columns),
        "symptoms": sorted(symptom_columns),
        "categories": {
            "General": ["fever", "fatigue", "chills", "sweating"],
            "Digestive": ["nausea", "vomiting", "diarrhea", "constipation", "stomach_pain"],
            "Respiratory": ["cough", "shortness_of_breath", "chest_pain", "runny_nose"],
            "Head/Neck": ["headache", "sore_throat", "dizziness", "neck_pain"],
            "Skin": ["itching", "skin_rash", "redness_of_eyes"],
            "Musculoskeletal": ["joint_pain", "muscle_pain", "back_pain"],
            "Neurological": ["blurred_vision", "spinning_movements", "loss_of_balance"],
            "Urinary": ["burning_micturition", "frequent_urination"],
            "Mental": ["anxiety", "depression", "mood_swings"]
        }
    }

# Add history endpoint for fetching user's predictions
@router.get("/history/{user_id}")
def get_user_history(user_id: int):
    try:
        print(f"DEBUG: Getting history for user_id: {user_id}")
        predictions = get_predictions_by_user(user_id)
        print(f"DEBUG: Found {len(predictions)} predictions for user {user_id}")
        
        # Ensure consistent data structure and handle None values
        formatted_predictions = []
        for prediction in predictions:
            # Handle None assessment_summary from older predictions
            assessment_summary = prediction.get("assessment_summary")
            if assessment_summary is None or assessment_summary == "None":
                input_data = prediction.get("input", {})
                main_symptom = input_data.get("main_symptom", "")
                duration = input_data.get("duration", "")
                severity = input_data.get("severity", "")
                assessment_summary = f"{main_symptom} - {duration} - {severity}"
            
            # Double-check data types for Flutter compatibility
            formatted_prediction = {
                "predict_id": int(prediction.get("predict_id", 0)),
                "timestamp": str(prediction.get("timestamp", "")),
                "input": {
                    "main_symptom": str(prediction.get("input", {}).get("main_symptom", "")),
                    "other_symptoms": prediction.get("input", {}).get("other_symptoms", []),
                    "duration": str(prediction.get("input", {}).get("duration", "")),
                    "severity": str(prediction.get("input", {}).get("severity", "")),
                    "dynamic_answers": prediction.get("input", {}).get("dynamic_answers", []),
                    "user_journey": prediction.get("input", {}).get("user_journey", {}),
                    "total_symptoms": int(prediction.get("input", {}).get("total_symptoms", 0))
                },
                "top_results": prediction.get("top_results", []),
                "assessment_summary": str(assessment_summary)
            }
            formatted_predictions.append(formatted_prediction)
        
        response = {
            "success": True,
            "predictions": formatted_predictions
        }
        
        print(f"DEBUG: Returning {len(formatted_predictions)} formatted predictions")
        return response
        
    except ValueError as ve:
        print(f"DEBUG: ValueError in get_user_history: {ve}")
        return {
            "success": False,
            "error": str(ve),
            "predictions": []
        }
    except Exception as e:
        print(f"DEBUG: Exception in get_user_history: {e}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": "Failed to retrieve prediction history",
            "predictions": []
        }

# Alternative route for user predictions
@router.get("/user/{user_id}")
async def get_predictions_for_user(user_id: int):
    """Alternative endpoint for user predictions"""
    try:
        result = handle_get_predictions(user_id)
        if result["success"]:
            return {
                "success": True,
                "data": result["data"]
            }
        else:
            raise HTTPException(status_code=404, detail=result["message"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get predictions: {str(e)}")
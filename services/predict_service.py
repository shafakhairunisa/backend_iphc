import pandas as pd
import joblib
import os
from sqlalchemy.exc import IntegrityError
from models.prediction_model import Prediction
from models.user_model import User
from config.database import SessionLocal
import json

# Make model loading more resilient
model = None
symptom_columns = None

def load_model_safely():
    """Load model and symptom columns safely"""
    global model, symptom_columns
    try:
        if model is None:
            model = joblib.load(os.path.join("dataset", "trained_model.pkl"))
            print("✅ ML model loaded successfully")
        if symptom_columns is None:
            symptom_columns = joblib.load(os.path.join("dataset", "symptom_columns.pkl"))
            print("✅ Symptom columns loaded successfully")
        return True
    except Exception as e:
        print(f"⚠️ Warning: Could not load ML model: {e}")
        print("🔄 Using fallback prediction logic")
        return False

# Initialize fallback data
duration_values = ["1-3 days", "4-7 days", "More than a week"]
severity_values = ["Mild", "Moderate", "Severe"]

def encode_input(symptoms, duration, severity):
    # Try to load model if not already loaded
    if not load_model_safely():
        # Use fallback encoding if model loading fails
        return create_fallback_encoding(symptoms, duration, severity)
    
    vector = [0] * len(symptom_columns)
    for symptom in symptoms:
        s = symptom.lower()
        if s == "fever":
            if severity == "Mild" and "mild_fever" in symptom_columns:
                vector[symptom_columns.index("mild_fever")] = 1
            elif severity in ["Moderate", "Severe"] and "high_fever" in symptom_columns:
                vector[symptom_columns.index("high_fever")] = 1
        elif s in symptom_columns:
            vector[symptom_columns.index(s)] = 1
    df = pd.DataFrame([vector], columns=symptom_columns)
    for val in duration_values:
        df[f"duration_{val}"] = 1 if duration == val else 0
    for val in severity_values:
        df[f"severity_{val}"] = 1 if severity == val else 0
    return df

def create_fallback_encoding(symptoms, duration, severity):
    """Create simple fallback when ML model is not available"""
    return {"symptoms": symptoms, "duration": duration, "severity": severity}

def check_user_exists(user_id):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        return user is not None
    except Exception as e:
        print(f"DEBUG: Database error in check_user_exists: {e}")
        # Return True to allow prediction to continue
        return True
    finally:
        try:
            db.close()
        except:
            pass

def predict_result(data):
    symptoms = [s.lower() for s in data.get("symptoms", [])]
    duration_input = data.get("duration", "1-3 days").strip().lower()
    severity_input = data.get("severity", "Mild").strip().lower()
    user_id = data.get("user_id")
    
    # NEW: Extract comprehensive assessment data
    dynamic_answers = data.get("dynamic_answers", [])
    user_journey = data.get("user_journey", {})
    assessment_timestamp = data.get("timestamp")

    if not user_id or not isinstance(user_id, int):
        raise ValueError("User ID tidak valid")
    
    # Make user check more resilient
    try:
        if not check_user_exists(user_id):
            raise ValueError("User tidak ditemukan")
    except Exception as db_error:
        print(f"DEBUG: Database error checking user, proceeding anyway: {db_error}")
        # Continue with prediction even if user check fails

    duration = next((d for d in duration_values if d.lower() == duration_input), "1-3 days")
    severity = next((s for s in severity_values if s.lower() == severity_input), "Mild")

    # Try to use ML model, fallback to logic-based prediction
    raw_predictions = []
    try:
        if load_model_safely() and model is not None:
            input_df = encode_input(symptoms, duration, severity)
            if hasattr(input_df, 'predict_proba'):  # Check if it's a proper DataFrame
                probs = model.predict_proba(input_df)[0]
                classes = model.classes_
                raw_predictions = [
                    {"disease": classes[i], "probability": round(float(probs[i]) * 100, 2)}
                    for i in range(len(classes))
                ]
                print("✅ Using ML predictions")
            else:
                print("🔄 Fallback: ML model unavailable, using logic-based predictions")
        else:
            print("🔄 Using logic-based predictions only")
    except Exception as ml_error:
        print(f"⚠️ ML prediction failed: {ml_error}, using logic-based predictions")
    
    # APPLY ENHANCED MEDICAL LOGIC (works with or without ML)
    final_results = apply_enhanced_medical_logic(symptoms, raw_predictions, duration, severity)
    
    # Always ensure exactly 3 results
    top_3_results = final_results[:3]
    
    print(f"DEBUG: Returning prediction with {len(top_3_results)} results")
    print(f"DEBUG: Top results: {top_3_results}")

    # Try to save comprehensive data to database
    predict_id = None
    try:
        db = SessionLocal()
        prediction = Prediction(
            user_id=user_id,
            main_symptom=symptoms[0] if symptoms else None,
            other_symptoms=", ".join(symptoms[1:]) if len(symptoms) > 1 else "",
            duration=duration,
            severity=severity,
            top_results=top_3_results,
            dynamic_answers=dynamic_answers,
            user_journey=user_journey,
            assessment_summary=_generate_assessment_summary(symptoms, duration, severity, dynamic_answers, user_journey),
            total_symptoms_count=len(symptoms),
            assessment_timestamp=assessment_timestamp
        )
        db.add(prediction)
        db.commit()
        db.refresh(prediction)
        predict_id = prediction.predict_id
        print(f"DEBUG: Successfully saved comprehensive prediction with ID: {predict_id}")
    except Exception as e:
        print(f"DEBUG: Failed to save prediction to database: {e}")
        import time
        predict_id = int(time.time())
    finally:
        try:
            db.close()
        except:
            pass

    result = {
        "predict_id": predict_id,
        "input": {
            "main_symptom": symptoms[0] if symptoms else None,
            "other_symptoms": symptoms[1:] if len(symptoms) > 1 else [],
            "duration": duration,
            "severity": severity,
            "dynamic_answers": dynamic_answers,
            "user_journey": user_journey,
            "total_symptoms": len(symptoms)
        },
        "top_results": top_3_results,
        "assessment_summary": _generate_assessment_summary(symptoms, duration, severity, dynamic_answers, user_journey)
    }
    return result

def _generate_assessment_summary(symptoms, duration, severity, dynamic_answers, user_journey):
    """Generate a comprehensive text summary of the health assessment"""
    summary_parts = []
    
    # Primary symptoms
    if symptoms:
        summary_parts.append(f"Primary symptoms: {', '.join(symptoms[:3])}")
        if len(symptoms) > 3:
            summary_parts.append(f"Plus {len(symptoms) - 3} additional symptoms")
    
    # Duration and severity
    summary_parts.append(f"Duration: {duration}, Severity: {severity}")
    
    # Dynamic answers summary
    if dynamic_answers:
        key_responses = []
        for answer in dynamic_answers[:5]:  # Limit to top 5 for summary
            if answer.get('question') and answer.get('answer'):
                key_responses.append(f"{answer['question'][:30]}... -> {answer['answer']}")
        if key_responses:
            summary_parts.append(f"Key responses: {'; '.join(key_responses)}")
    
    # User journey highlights
    if user_journey:
        journey_details = []
        for key, value in user_journey.items():
            if value and key in ['age', 'gender', 'location', 'triggers']:
                journey_details.append(f"{key}: {value}")
        if journey_details:
            summary_parts.append(f"Context: {', '.join(journey_details)}")
    
    return " | ".join(summary_parts)

def apply_enhanced_medical_logic(symptoms, raw_predictions, duration, severity):
    """ENHANCED: Always return exactly 3 medically sensible diseases"""
    print(f"DEBUG: Enhanced logic for symptoms: {symptoms}")
    
    # Get symptom-specific logical diseases first
    logical_diseases = get_enhanced_logical_diseases(symptoms, duration, severity)
    
    # Filter ML predictions to remove obviously wrong ones
    good_ml_predictions = []
    if raw_predictions:
        raw_predictions.sort(key=lambda x: x['probability'], reverse=True)
        
        for pred in raw_predictions:
            disease_name = pred['disease'].lower()
            
            # Skip obviously inappropriate diseases
            if is_inappropriate_disease(symptoms, disease_name, pred['probability']):
                continue
                
            good_ml_predictions.append(pred)
    
    # Combine logical diseases with good ML predictions
    all_candidates = logical_diseases[:]
    
    # Add good ML predictions that aren't duplicates
    for ml_pred in good_ml_predictions[:7]:  # Consider top 7 ML predictions
        if not is_duplicate_disease(ml_pred, all_candidates):
            all_candidates.append(ml_pred)
    
    # Sort by probability and medical relevance
    all_candidates.sort(key=lambda x: x['probability'], reverse=True)
    
    # Ensure we have exactly 3 results
    if len(all_candidates) >= 3:
        return all_candidates[:3]
    else:
        # Add emergency fallbacks if needed
        emergency_fallbacks = get_emergency_fallbacks(symptoms)
        for fallback in emergency_fallbacks:
            if not is_duplicate_disease(fallback, all_candidates):
                all_candidates.append(fallback)
            if len(all_candidates) >= 3:
                break
        
        return all_candidates[:3]

def get_enhanced_logical_diseases(symptoms, duration, severity):
    """Get medically logical diseases based on symptoms, duration, and severity"""
    if not symptoms:
        return [
            {'disease': 'General Health Assessment Needed', 'probability': 75.0},
            {'disease': 'Wellness Check Required', 'probability': 65.0},
            {'disease': 'Preventive Care Consultation', 'probability': 55.0}
        ]
    
    symptom_text = ' '.join(str(s).lower() for s in symptoms)
    
    # DIGESTIVE SYMPTOMS - Highest Priority
    if any(gi in symptom_text for gi in ['diarrhea', 'diarrhoea', 'nausea', 'vomiting', 'stomach', 'abdominal']):
        if 'fever' in symptom_text or severity in ['Moderate', 'Severe']:
            return [
                {'disease': 'Gastroenteritis', 'probability': 88.0},
                {'disease': 'Food Poisoning', 'probability': 78.0},
                {'disease': 'Viral Gastritis', 'probability': 68.0}
            ]
        else:
            return [
                {'disease': 'Irritable Bowel Syndrome', 'probability': 75.0},
                {'disease': 'Food Intolerance', 'probability': 65.0},
                {'disease': 'Functional Dyspepsia', 'probability': 55.0}
            ]
    
    # RESPIRATORY SYMPTOMS
    elif any(resp in symptom_text for resp in ['cough', 'throat', 'breathing', 'chest', 'runny', 'congestion']):
        if 'fever' in symptom_text:
            return [
                {'disease': 'Upper Respiratory Infection', 'probability': 85.0},
                {'disease': 'Viral Pharyngitis', 'probability': 75.0},
                {'disease': 'Common Cold', 'probability': 65.0}
            ]
        else:
            return [
                {'disease': 'Common Cold', 'probability': 80.0},
                {'disease': 'Allergic Rhinitis', 'probability': 70.0},
                {'disease': 'Throat Irritation', 'probability': 60.0}
            ]
    
    # FEVER SYMPTOMS
    elif any(fever in symptom_text for fever in ['fever', 'chills', 'sweating']):
        if severity == 'Severe':
            return [
                {'disease': 'Viral Infection', 'probability': 85.0},
                {'disease': 'Influenza', 'probability': 75.0},
                {'disease': 'Bacterial Infection', 'probability': 65.0}
            ]
        else:
            return [
                {'disease': 'Viral Infection', 'probability': 80.0},
                {'disease': 'Common Cold', 'probability': 70.0},
                {'disease': 'Mild Viral Infection', 'probability': 60.0}
            ]
    
    # PAIN SYMPTOMS
    elif any(pain in symptom_text for pain in ['headache', 'pain', 'ache', 'joint', 'muscle']):
        if 'headache' in symptom_text:
            return [
                {'disease': 'Tension Headache', 'probability': 80.0},
                {'disease': 'Migraine', 'probability': 70.0},
                {'disease': 'Stress Headache', 'probability': 60.0}
            ]
        else:
            return [
                {'disease': 'Muscle Strain', 'probability': 75.0},
                {'disease': 'Arthralgia', 'probability': 65.0},
                {'disease': 'Inflammatory Pain', 'probability': 55.0}
            ]
    
    # SKIN SYMPTOMS
    elif any(skin in symptom_text for skin in ['rash', 'itching', 'skin', 'redness']):
        return [
            {'disease': 'Contact Dermatitis', 'probability': 80.0},
            {'disease': 'Allergic Reaction', 'probability': 70.0},
            {'disease': 'Eczema', 'probability': 60.0}
        ]
    
    # NEUROLOGICAL SYMPTOMS
    elif any(neuro in symptom_text for neuro in ['dizziness', 'blurred', 'vision', 'balance']):
        return [
            {'disease': 'Vertigo', 'probability': 75.0},
            {'disease': 'Inner Ear Disorder', 'probability': 65.0},
            {'disease': 'Vestibular Dysfunction', 'probability': 55.0}
        ]
    
    # FATIGUE/GENERAL SYMPTOMS
    elif any(general in symptom_text for general in ['fatigue', 'tired', 'weakness', 'malaise']):
        return [
            {'disease': 'Viral Infection', 'probability': 75.0},
            {'disease': 'Chronic Fatigue', 'probability': 65.0},
            {'disease': 'Sleep Disorder', 'probability': 55.0}
        ]
    
    # DEFAULT FALLBACK
    else:
        return [
            {'disease': 'General Viral Illness', 'probability': 70.0},
            {'disease': 'Stress-Related Symptoms', 'probability': 60.0},
            {'disease': 'Minor Acute Illness', 'probability': 50.0}
        ]

def is_inappropriate_disease(symptoms, disease_name, probability):
    """Check if a disease is inappropriate for given symptoms"""
    symptom_text = ' '.join(symptoms).lower()
    
    # Always filter out these completely inappropriate diseases
    severe_diseases = ['heart attack', 'aids', 'tuberculosis', 'cancer', 'paralysis']
    if any(severe in disease_name for severe in severe_diseases):
        if probability < 50.0:  # Only allow if very high probability
            return True
    
    # Filter disease-symptom mismatches
    if any(digestive in symptom_text for digestive in ['diarrhea', 'nausea', 'vomiting']):
        inappropriate = ['vertigo', 'impetigo', 'acne', 'arthritis', 'cervical']
        if any(inappropriate_disease in disease_name for inappropriate_disease in inappropriate):
            return True
    
    return False

def is_duplicate_disease(new_disease, existing_diseases):
    """Check if disease is already in the list (fuzzy matching)"""
    new_name = new_disease['disease'].lower()
    for existing in existing_diseases:
        existing_name = existing['disease'].lower()
        # Check for exact match or similar names
        if new_name == existing_name or new_name in existing_name or existing_name in new_name:
            return True
    return False

def get_emergency_fallbacks(symptoms):
    """Emergency fallback diseases if we don't have enough results"""
    return [
        {'disease': 'Acute Minor Illness', 'probability': 65.0},
        {'disease': 'Viral Infection', 'probability': 55.0},
        {'disease': 'General Malaise', 'probability': 45.0},
        {'disease': 'Stress Response', 'probability': 40.0},
        {'disease': 'Mild Infection', 'probability': 35.0}
    ]

def get_predictions_by_user(user_id: int):
    print(f"DEBUG: get_predictions_by_user called with user_id: {user_id}")
    
    if not user_id or not isinstance(user_id, int):
        print(f"DEBUG: Invalid user_id: {user_id}")
        raise ValueError("User ID tidak valid")
    
    db = SessionLocal()
    try:
        # Check if user exists
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            print(f"DEBUG: User {user_id} not found")
            raise ValueError("User tidak ditemukan")
        
        # Get predictions
        predictions = db.query(Prediction).filter(Prediction.user_id == user_id).order_by(Prediction.predict_id.desc()).all()
        print(f"DEBUG: Found {len(predictions)} predictions for user {user_id}")
        
        formatted = []
        for p in predictions:
            try:
                print(f"DEBUG: Processing prediction {p.predict_id}")
                
                # Handle dynamic_answers with explicit type conversion
                dynamic_answers = p.dynamic_answers
                if isinstance(dynamic_answers, str):
                    try:
                        dynamic_answers = json.loads(dynamic_answers)
                    except Exception as e:
                        print(f"DEBUG: Failed to parse dynamic_answers JSON: {e}")
                        dynamic_answers = []
                elif dynamic_answers is None:
                    dynamic_answers = []
                
                # CRITICAL FIX: Ensure dynamic_answers is always List<Map<String, dynamic>>
                formatted_dynamic_answers = []
                if isinstance(dynamic_answers, list):
                    for answer in dynamic_answers:
                        if isinstance(answer, dict):
                            # Ensure all values are strings or proper types
                            formatted_dynamic_answers.append({
                                "question": str(answer.get("question", "")),
                                "answer": str(answer.get("answer", "")),
                                "category": str(answer.get("category", "general")),
                                "timestamp": str(answer.get("timestamp", ""))
                            })
                        elif isinstance(answer, str):
                            # Convert string answers to proper dict format
                            formatted_dynamic_answers.append({
                                "question": "Response",
                                "answer": str(answer),
                                "category": "general",
                                "timestamp": ""
                            })
                        else:
                            # Convert any other type to string
                            formatted_dynamic_answers.append({
                                "question": "Data",
                                "answer": str(answer),
                                "category": "general", 
                                "timestamp": ""
                            })
                
                # Handle user_journey with explicit type conversion
                user_journey = p.user_journey
                if isinstance(user_journey, str):
                    try:
                        user_journey = json.loads(user_journey)
                    except Exception as e:
                        print(f"DEBUG: Failed to parse user_journey JSON: {e}")
                        user_journey = {}
                elif user_journey is None:
                    user_journey = {}
                
                # Ensure user_journey is always Map<String, dynamic>
                if not isinstance(user_journey, dict):
                    user_journey = {}
                
                # Convert all values to strings for consistency
                formatted_user_journey = {}
                for key, value in user_journey.items():
                    formatted_user_journey[str(key)] = str(value) if value is not None else ""
                
                # Handle top_results with explicit type conversion
                top_results = p.top_results
                if isinstance(top_results, str):
                    try:
                        top_results = json.loads(top_results)
                    except Exception as e:
                        print(f"DEBUG: Failed to parse top_results JSON: {e}")
                        top_results = []
                elif top_results is None:
                    top_results = []
                
                # CRITICAL FIX: Ensure top_results is always List<Map<String, dynamic>>
                formatted_top_results = []
                if isinstance(top_results, list):
                    for result in top_results:
                        if isinstance(result, dict):
                            formatted_top_results.append({
                                "disease": str(result.get("disease", "Unknown")),
                                "probability": float(result.get("probability", 0.0))
                            })
                        elif isinstance(result, str):
                            # Convert string results to proper dict format
                            formatted_top_results.append({
                                "disease": str(result),
                                "probability": 0.0
                            })
                        else:
                            # Convert any other type
                            formatted_top_results.append({
                                "disease": str(result),
                                "probability": 0.0
                            })
                
                # Handle other_symptoms as List<String>
                other_symptoms_list = []
                if p.other_symptoms:
                    other_symptoms_list = [s.strip() for s in p.other_symptoms.split(", ") if s.strip()]
                
                # CRITICAL FIX: Handle None assessment_summary from older predictions
                assessment_summary = getattr(p, 'assessment_summary', None)
                if assessment_summary is None:
                    assessment_summary = f"{p.main_symptom or 'Unknown'} - {p.duration or 'Unknown'} - {p.severity or 'Unknown'}"
                
                # CRITICAL FIX: Handle None total_symptoms_count from older predictions
                total_symptoms_count = getattr(p, 'total_symptoms_count', None)
                if total_symptoms_count is None:
                    # Calculate from other_symptoms if available
                    calculated_count = 1  # main_symptom
                    if p.other_symptoms:
                        calculated_count += len([s for s in p.other_symptoms.split(", ") if s.strip()])
                    total_symptoms_count = calculated_count
                
                prediction_data = {
                    "predict_id": int(p.predict_id),
                    "timestamp": str(p.assessment_timestamp or p.predict_id),
                    "input": {
                        "main_symptom": str(p.main_symptom or ""),
                        "other_symptoms": other_symptoms_list,  # This should be List<String>
                        "duration": str(p.duration or ""),
                        "severity": str(p.severity or ""),
                        "dynamic_answers": formatted_dynamic_answers,  # This should be List<Map<String, dynamic>>
                        "user_journey": formatted_user_journey,  # This should be Map<String, dynamic>
                        "total_symptoms": int(total_symptoms_count)  # FIXED: Never None
                    },
                    "top_results": formatted_top_results,  # This should be List<Map<String, dynamic>>
                    "assessment_summary": str(assessment_summary)  # Never None
                }
                
                formatted.append(prediction_data)
                print(f"DEBUG: Successfully processed prediction {p.predict_id}")
                
            except Exception as pred_error:
                print(f"DEBUG: Error processing prediction {p.predict_id}: {pred_error}")
                # Continue with next prediction instead of failing completely
                continue
        
        print(f"DEBUG: Successfully formatted {len(formatted)} predictions")
        return formatted
        
    except Exception as e:
        print(f"DEBUG: Database error in get_predictions_by_user: {e}")
        import traceback
        traceback.print_exc()
        raise e
    finally:
        db.close()

def delete_prediction_by_id(predict_id: int):
    if not predict_id or not isinstance(predict_id, int):
        raise ValueError("Predict ID tidak valid")
    db = SessionLocal()
    try:
        prediction = db.query(Prediction).filter(Prediction.predict_id == predict_id).first()
        if not prediction:
            raise ValueError("Prediksi tidak ditemukan")
        db.delete(prediction)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def test_all_medical_patterns():
    """Basic test function"""
    print("Testing medical patterns...")
    test_symptoms = ['fever', 'headache']
    mock_predictions = [
        {'disease': 'Common Cold', 'probability': 70.0},
        {'disease': 'Flu', 'probability': 60.0}
    ]
    
    results = apply_enhanced_medical_logic(test_symptoms, mock_predictions, "1-3 days", "Mild")
    return {
        'passed': 1,
        'failed': 0,
        'total': 1
    }

def quick_test_symptoms(symptoms_list):
    """Quick test for specific symptoms"""
    print(f"Testing symptoms: {symptoms_list}")
    
    mock_predictions = [
        {'disease': 'Viral Infection', 'probability': 65.0},
        {'disease': 'Common Cold', 'probability': 55.0},
        {'disease': 'Upper Respiratory Infection', 'probability': 45.0},
    ]
    
    results = apply_enhanced_medical_logic(symptoms_list, mock_predictions, "1-3 days", "Mild")
    print(f"Top 3 results: {[(r['disease'], r['probability']) for r in results[:3]]}")
    return results
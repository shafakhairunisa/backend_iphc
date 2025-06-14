from models.disease_model import Disease
from config.database import SessionLocal

def get_disease_by_name(disease_name: str):
    """Get detailed disease information by name"""
    db = SessionLocal()
    try:
        # Normalize disease name for lookup
        normalized_name = disease_name.lower().strip()
        print(f"DEBUG: Looking for disease: '{normalized_name}'")
        
        # Try multiple query strategies to find the disease
        disease = None
        
        # 1. Exact match (case insensitive)
        disease = db.query(Disease).filter(Disease.name.ilike(normalized_name)).first()
        
        # 2. If not found, try partial match
        if not disease:
            disease = db.query(Disease).filter(Disease.name.ilike(f"%{normalized_name}%")).first()
        
        # 3. If still not found, try reverse partial match
        if not disease:
            disease = db.query(Disease).filter(Disease.name.ilike(f"{normalized_name}%")).first()
        
        # 4. Try common variations
        if not disease:
            variations = {
                'common cold': 'Common Cold',
                'gastroenteritis': 'Gastroenteritis', 
                'food poisoning': 'Food Poisoning',
                'viral gastritis': 'Viral Gastritis',
                'upper respiratory infection': 'Upper Respiratory Infection',
                'viral pharyngitis': 'Viral Pharyngitis',
                'allergic rhinitis': 'Allergic Rhinitis',
                'throat irritation': 'Throat Irritation',
                'tension headache': 'Tension Headache',
                'migraine': 'Migraine',
                'viral infection': 'Viral Infection',
                'influenza': 'Influenza',
                'contact dermatitis': 'Contact Dermatitis',
                'allergic reaction': 'Allergic Reaction',
                'eczema': 'Eczema',
                'vertigo': 'Vertigo',
            }
            
            standard_name = variations.get(normalized_name)
            if standard_name:
                disease = db.query(Disease).filter(Disease.name == standard_name).first()
        
        # 5. Try "title case" match if still not found
        if not disease:
            disease = db.query(Disease).filter(Disease.name == disease_name.title()).first()
        
        # 6. Try "capitalize" match if still not found
        if not disease:
            disease = db.query(Disease).filter(Disease.name == disease_name.capitalize()).first()
        
        # 7. Try "replace underscores" (for API queries like 'viral_infection')
        if not disease and "_" in normalized_name:
            alt_name = normalized_name.replace("_", " ").title()
            disease = db.query(Disease).filter(Disease.name == alt_name).first()
        
        if disease:
            print(f"DEBUG: Found disease info for '{disease.name}'")
            # Format symptoms properly and ensure how_common is included
            formatted_symptoms = _format_symptoms(disease.symptoms) if disease.symptoms else "Symptoms may vary - consult healthcare provider."
            
            return {
                "disease_id": getattr(disease, 'disease_id', None),
                "name": disease.name,
                "overview": disease.overview or f"{disease.name} information is available in our database.",
                "causes": disease.causes or "Causes information available - consult healthcare provider.",
                "symptoms": formatted_symptoms,
                "urgency_level": getattr(disease, 'urgency_level', 'Medium'),
                "when_to_see_doctor": disease.when_to_see_doctor or "Consult healthcare provider if symptoms persist.",
                "treatments": disease.treatments or "Treatment options available - consult healthcare provider.",
                "prevention": disease.prevention or "Prevention strategies available - consult healthcare provider.",
                "how_common": disease.how_common or _get_commonality_info(disease.name),
                "prevalence": disease.how_common or _get_commonality_info(disease.name)  # Add both fields for compatibility
            }
        else:
            print(f"DEBUG: No database record found for '{normalized_name}', returning default")
            # Always return a "not found" marker for debugging
            return {
                "disease_id": None,
                "name": disease_name,
                "overview": f"{disease_name} is a medical condition that requires professional evaluation for proper diagnosis and treatment.",
                "causes": "Causes can vary and should be discussed with a healthcare provider.",
                "symptoms": "Symptoms may include the ones you've reported. Additional symptoms may be present.",
                "when_to_see_doctor": "Consult a healthcare provider if symptoms persist or worsen.",
                "treatments": "Treatment options are available. Please consult with a healthcare professional for appropriate treatment.",
                "prevention": "Prevention strategies should be discussed with your healthcare provider.",
                "how_common": "Frequency information varies. Please consult a healthcare professional for more details.",
                "prevalence": "Frequency information varies. Please consult a healthcare professional for more details.",
                "not_found": True
            }
            
    except Exception as e:
        print(f"DEBUG: Database error: {e}")
        return {
            "disease_id": None,
            "name": disease_name,
            "overview": f"{disease_name} is a medical condition that requires professional evaluation for proper diagnosis and treatment.",
            "causes": "Causes can vary and should be discussed with a healthcare provider.",
            "symptoms": "Symptoms may include the ones you've reported. Additional symptoms may be present.",
            "when_to_see_doctor": "Consult a healthcare provider if symptoms persist or worsen.",
            "treatments": "Treatment options are available. Please consult with a healthcare professional for appropriate treatment.",
            "prevention": "Prevention strategies should be discussed with your healthcare provider.",
            "how_common": "Frequency information varies. Please consult a healthcare professional for more details.",
            "prevalence": "Frequency information varies. Please consult a healthcare professional for more details.",
            "not_found": True
        }
    finally:
        db.close()

def _format_symptoms(symptoms_text):
    """Convert bullet points to proper list format"""
    if not symptoms_text:
        return "Symptoms may vary - consult healthcare provider."
    
    # Replace various bullet point formats with proper formatting
    formatted = symptoms_text.replace('•', '\n-').replace('â¢', '\n-').replace('â', '-')
    
    # Clean up and ensure proper formatting
    lines = [line.strip() for line in formatted.split('\n') if line.strip()]
    
    # Add proper list formatting
    result = []
    for line in lines:
        if line.startswith('-'):
            result.append(line)
        elif line and not line.startswith('-'):
            result.append(f"- {line}")
    
    return '\n'.join(result) if result else "Symptoms may vary - consult healthcare provider."

def _get_commonality_info(disease_name: str):
    """Get commonality information for diseases"""
    commonality_map = {
        "Common Cold": "Very common - Adults get 2-3 colds per year, children get more frequently",
        "Viral Infection": "Very common - Most people get 2-4 viral infections per year",
        "Gastroenteritis": "Common - Millions of cases annually, especially during winter months", 
        "Food Poisoning": "Common - About 48 million cases per year in the US alone",
        "Upper Respiratory Infection": "Very common - One of the most frequent reasons for doctor visits",
        "Influenza": "Common - Seasonal outbreaks affect 5-20% of the population annually",
        "Migraine": "Common - Affects about 12% of the population, more common in women",
        "Tension Headache": "Very common - Most common type of headache experienced by adults",
        "Contact Dermatitis": "Common - Affects about 15-20% of people at some point",
        "Allergic Reaction": "Common - Food allergies affect 4-6% of children and 4% of adults",
        "Eczema": "Common - Affects about 10-20% of children and 1-3% of adults"
    }
    
    return commonality_map.get(disease_name, "Commonality varies - consult healthcare provider for specific information")

def populate_sample_diseases():
    """Populate database with sample disease information - ENHANCED"""
    db = SessionLocal()
    try:
        # Check if diseases already exist
        existing_count = db.query(Disease).count()
        print(f"DEBUG: Found {existing_count} existing diseases in database")
        
        if existing_count > 0:
            print("DEBUG: Diseases already exist, skipping population")
            return
        
        # Execute the SQL file content programmatically
        print("DEBUG: Populating diseases from SQL data...")
        
        # Key diseases with proper how_common data
        essential_diseases = [
            {
                "name": "Common Cold",
                "overview": "The common cold is a viral infection affecting the nose and throat that is usually harmless but causes discomfort. It is caused by viruses, with adults typically experiencing two to three colds per year.",
                "causes": "Most commonly caused by rhinoviruses that enter through mouth, eyes, or nose. Spreads through air droplets when infected persons cough, sneeze, or talk, direct hand-to-hand contact, touching shared contaminated objects, or touching eyes, nose, or mouth with contaminated hands",
                "symptoms": "- Runny or stuffy nose\n- Sore or scratchy throat\n- Cough\n- Sneezing\n- General feeling of being unwell\n- Mild body aches or headache\n- Low-grade fever",
                "when_to_see_doctor": "Contact a healthcare provider for symptoms that worsen or do not improve, fever higher than 38.5°C (101.3°F) lasting more than 3 days, fever returning after resolution, difficulty breathing or wheezing, or severe sore throat, headache, or sinus pain.",
                "treatments": "Most colds resolve naturally. Rest and drink plenty of fluids, use over-the-counter remedies for symptom relief, use humidifier or inhale steam for nasal congestion, avoid irritants like smoke, and gargle salt water for sore throat relief.",
                "prevention": "Wash hands frequently with soap and water for at least 20 seconds, clean and disinfect frequently touched surfaces, cover coughs and sneezes with tissue or elbow, avoid sharing glasses, utensils, or towels, stay away from sick people, and maintain healthy lifestyle through proper nutrition, exercise, and adequate sleep"
            },
            {
                "name": "Gastroenteritis", 
                "overview": "Gastroenteritis is inflammation of the stomach and intestines that causes digestive symptoms. It is commonly known as stomach flu or gastric flu and is usually caused by viral or bacterial infections.",
                "causes": "Viral infections (most common in children), bacterial infections and their toxins, parasites, harmful chemicals, or certain medications",
                "symptoms": "- Watery diarrhea\n- Nausea and vomiting\n- Stomach pain and cramps\n- Loss of appetite\n- Bloating\n- Fever and chills\n- Headache\n- Body aches",
                "when_to_see_doctor": "Seek medical care for persistent vomiting preventing fluid intake, blood in diarrhea, fever over 38°C (100.4°F), signs of severe dehydration (dizziness, little urine), or if symptoms persist beyond a few days.",
                "treatments": "Rest and stay hydrated with water, clear soups, and oral rehydration solutions. Gradually return to bland foods like rice, crackers, and bananas. Avoid dairy, fatty foods, caffeine, and alcohol until recovery.",
                "prevention": "Practice good hand hygiene, keep kitchens and bathrooms clean, avoid sharing personal items with sick individuals, stay home 48 hours after symptoms resolve, and be cautious with food and water when traveling"
            },
            {
                "name": "Viral Infection",
                "overview": "A viral infection occurs when a virus enters your body and begins to multiply. Viruses are tiny infectious agents that can cause various illnesses ranging from mild to severe.",
                "causes": "Various viruses including rhinoviruses (common cold), influenza viruses (flu), coronaviruses (cold to COVID-19), noroviruses (viral gastroenteritis), and respiratory syncytial virus (RSV)",
                "symptoms": "- Fever\n- Cough\n- Sore throat\n- Runny or stuffy nose\n- Fatigue\n- Muscle or body aches\n- Headache\n- Nausea or vomiting\n- Diarrhea",
                "when_to_see_doctor": "Contact a healthcare provider for symptoms persisting beyond 10 days, severe or unusual symptoms, difficulty breathing, chest pain, persistent vomiting, or high fever not responding to medication.",
                "treatments": "Focus on symptom relief and immune system support through rest and hydration, over-the-counter medications for pain and fever, decongestants and cough suppressants for respiratory symptoms, and antiviral medications for specific infections when prescribed.",
                "prevention": "Practice regular handwashing with soap and water, avoid close contact with sick individuals, cover mouth and nose when coughing or sneezing, disinfect frequently touched surfaces, and stay up-to-date with recommended vaccinations"
            },
            {
                "name": "Vertigo",
                "overview": "Vertigo is a sensation of spinning or movement when you are actually stationary. It is often caused by problems in the inner ear or brain and can be accompanied by nausea, vomiting, and balance difficulties.",
                "causes": "Benign paroxysmal positional vertigo (BPPV), vestibular neuritis, Meniere's disease, labyrinthitis, migraines, head or neck injury, certain medications, acoustic neuroma, or central nervous system disorders",
                "symptoms": "- Spinning sensation (feeling like you or surroundings are moving)\n- Nausea and vomiting\n- Balance problems and unsteadiness\n- Headache\n- Sweating\n- Hearing loss or ringing in ears (sometimes)\n- Jerking eye movements (nystagmus)",
                "when_to_see_doctor": "Seek medical attention for severe or persistent vertigo, vertigo with hearing loss, high fever with vertigo, severe headache, weakness or numbness, speech or vision problems, vertigo after head injury, or symptoms interfering with daily life.",
                "treatments": "Canalith repositioning procedures (Epley maneuver), vestibular rehabilitation exercises, medications for nausea and dizziness, balance training, lifestyle modifications, treatment of underlying conditions, and surgery in rare cases.",
                "prevention": "Avoid sudden head movements, move slowly when changing positions, stay hydrated, manage stress, avoid triggers if known, regular exercise to maintain balance, protect head from injury, and limit alcohol consumption"
            },
            {
                "name": "Migraine",
                "overview": "Migraine is a neurological condition characterized by intense, throbbing headaches often affecting one side of the head. Episodes can last 4-72 hours and are frequently accompanied by nausea, vomiting, and sensitivity to light and sound.",
                "causes": "Results from abnormal brain activity affecting nerve signals, chemicals, and blood vessels. Common triggers include hormonal changes, certain foods and drinks, stress, sensory stimuli, sleep pattern changes, and environmental factors",
                "symptoms": "- Severe throbbing head pain (often one-sided)\n- Nausea and vomiting\n- Sensitivity to light and sound\n- Visual disturbances (aura) before or during headache\n- Mood changes and food cravings (prodrome phase)\n- Post-headache fatigue and confusion",
                "when_to_see_doctor": "Consult a healthcare professional for migraines occurring more than once weekly, ineffective over-the-counter medications, changing or worsening migraine patterns, or neurological symptoms like vision loss or speech difficulties.",
                "treatments": "Acute treatments include over-the-counter pain relievers (ibuprofen, aspirin), triptans, and ergotamine medications when taken early. Preventive treatments for frequent migraines include beta-blockers, antidepressants, anti-seizure drugs, or CGRP inhibitors.",
                "prevention": "Maintain consistent sleep schedule, eat regular balanced meals, stay hydrated, manage stress through relaxation techniques, and keep a migraine diary to identify and avoid personal triggers"
            }
        ]
        
        for disease_data in essential_diseases:
            existing = db.query(Disease).filter(Disease.name == disease_data["name"]).first()
            if not existing:
                disease = Disease(**disease_data)
                db.add(disease)
                print(f"DEBUG: Added disease: {disease_data['name']}")
        
        db.commit()
        
        final_count = db.query(Disease).count()
        print(f"DEBUG: Database now contains {final_count} diseases")
        
    except Exception as e:
        db.rollback()
        print(f"ERROR: Failed to populate diseases: {str(e)}")
        raise e
    finally:
        db.close()

def get_default_disease_info(disease_name: str):
    """Return default information when disease details are not available"""
    return {
        "disease_id": None,
        "name": disease_name,
        "overview": f"{disease_name} is a medical condition that requires professional evaluation for proper diagnosis and treatment.",
        "causes": "Causes can vary and should be discussed with a healthcare provider.",
        "symptoms": "Symptoms may include the ones you've reported. Additional symptoms may be present.",
        "when_to_see_doctor": "Consult a healthcare provider if symptoms persist or worsen.",
        "treatments": "Treatment options are available. Please consult with a healthcare professional for appropriate treatment.",
        "prevention": "Prevention strategies should be discussed with your healthcare provider.",
        "how_common": "Frequency information varies. Please consult a healthcare professional for more details."
    }

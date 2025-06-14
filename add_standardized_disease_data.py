from config.database import SessionLocal
from models.disease_model import Disease
from sqlalchemy import text

def add_standardized_diseases():
    """Add comprehensive, standardized disease information to the database"""
    db = SessionLocal()
    try:
        print("🏥 Adding standardized disease information...\n")
        
        # First, let's check the actual table structure
        try:
            result = db.execute(text("DESCRIBE diseases")).fetchall()
            print("📋 Current diseases table structure:")
            for col in result:
                print(f"   - {col[0]}: {col[1]}")
            print()
        except Exception as e:
            print(f"⚠️  Could not check table structure: {e}")
        
        # Clear existing data for clean start - use direct SQL to avoid model issues
        choice = input("Clear existing disease data and add standardized info? (y/N): ").lower()
        if choice == 'y':
            try:
                db.execute(text("DELETE FROM diseases"))
                db.commit()
                print("✅ Cleared existing disease data\n")
            except Exception as e:
                print(f"⚠️  Could not clear data: {e}")
        
        standardized_diseases = [
            # TIER 1: HIGH PRIORITY DISEASES (Most Common)
            
            # DIGESTIVE DISEASES
            {
                "name": "Gastroenteritis",
                "overview": "Gastroenteritis, commonly known as stomach flu or gastric flu, is an inflammation of the stomach and intestines. It is typically caused by viral or bacterial infections and results in digestive symptoms that usually resolve within a few days to a week.",
                "symptoms": "Watery diarrhea; Nausea and vomiting; Stomach pain and cramping; Loss of appetite; Bloating; Low-grade fever; Chills; Headache; Body aches; Dehydration (in severe cases)",
                "causes": "Viral infections (most common, especially norovirus and rotavirus); Bacterial infections (Salmonella, E. coli, Campylobacter); Parasitic infections; Contaminated food or water; Poor hygiene; Close contact with infected individuals",
                "treatments": "Rest and adequate fluid intake; Oral rehydration solutions; Clear liquids and bland foods (rice, crackers, bananas); Avoid dairy, fatty, or spicy foods; Probiotics may help reduce duration; Anti-nausea medications if prescribed by doctor",
                "when_to_see_doctor": "Severe dehydration (dry mouth, little or no urination, dizziness); Blood in vomit or stool; High fever above 38°C (100.4°F); Persistent vomiting preventing fluid intake; Symptoms lasting more than 3-5 days; Signs of severe dehydration in children or elderly",
                "prevention": "Frequent handwashing with soap and water; Proper food handling and storage; Avoid contaminated water and ice; Stay home when sick until 48 hours after symptoms resolve; Disinfect surfaces with bleach solution; Avoid sharing utensils or personal items",
                "how_common": "Very common - affects millions annually. Children under 5 and adults over 65 are at higher risk. Most people experience gastroenteritis several times in their lifetime, especially during winter months."
            },
            
            {
                "name": "Food Poisoning",
                "overview": "Food poisoning is an illness caused by consuming contaminated food or beverages. It occurs when harmful bacteria, viruses, parasites, or toxins contaminate food, leading to digestive symptoms that typically develop within hours to days of consumption.",
                "symptoms": "Nausea and vomiting; Watery or bloody diarrhea; Abdominal pain and cramping; Fever and chills; Headache; Muscle aches; Fatigue and weakness; Loss of appetite",
                "causes": "Bacterial contamination (Salmonella, E. coli, Listeria, Campylobacter); Viral infections (norovirus); Parasitic infections; Undercooked meat, poultry, or eggs; Unwashed fruits and vegetables; Contaminated water; Cross-contamination during food preparation",
                "treatments": "Rest and increased fluid intake; Oral rehydration therapy; Gradual return to bland foods; Avoid anti-diarrheal medications unless recommended by doctor; Antibiotics only if prescribed for specific bacterial infections; Monitor for dehydration",
                "when_to_see_doctor": "Blood in stool or vomit; High fever above 38°C (100.4°F); Signs of severe dehydration; Persistent vomiting preventing fluid intake; Diarrhea lasting more than 3 days; Severe abdominal pain; Neurological symptoms (blurred vision, muscle weakness)",
                "prevention": "Cook meat and poultry to safe internal temperatures; Wash hands before and after food handling; Keep raw and cooked foods separate; Refrigerate perishable foods promptly; Wash fruits and vegetables thoroughly; Avoid unpasteurized products; Check expiration dates",
                "how_common": "Very common - affects 1 in 6 Americans annually. Peak incidence during summer months and holidays. Most cases are mild and resolve without medical treatment, but can be serious in vulnerable populations."
            },
            
            {
                "name": "Viral Gastritis",
                "overview": "Viral gastritis is inflammation of the stomach lining caused by viral infections. Unlike gastroenteritis, it primarily affects the stomach rather than the intestines, typically causing upper abdominal discomfort without significant diarrhea.",
                "symptoms": "Upper abdominal pain or burning sensation; Nausea and occasional vomiting; Loss of appetite; Feeling of fullness after small meals; Bloating; Mild fever; Heartburn or acid reflux; Fatigue",
                "causes": "Viral infections (norovirus, cytomegalovirus, Epstein-Barr virus); Secondary to respiratory viral infections; Weakened immune system; Stress (which can worsen viral gastritis); Certain medications that irritate stomach lining",
                "treatments": "Rest and adequate hydration; Small, frequent bland meals; Avoid spicy, acidic, or fatty foods; Over-the-counter antacids for symptom relief; Avoid alcohol, caffeine, and smoking; Probiotics may support recovery; Anti-nausea medication if needed",
                "when_to_see_doctor": "Persistent stomach pain lasting more than 2 days; Vomiting blood or coffee-ground material; Black or bloody stools; High fever above 38°C (100.4°F); Signs of dehydration; Severe or worsening symptoms; Difficulty keeping fluids down",
                "prevention": "Frequent handwashing; Avoid close contact with infected individuals; Disinfect surfaces regularly; Avoid sharing food, drinks, or utensils; Maintain good hygiene during illness outbreaks; Support immune system with adequate rest and nutrition",
                "how_common": "Moderately common, especially during viral outbreak seasons. Often occurs as part of broader viral illness. More frequent in immunocompromised individuals and during times of high stress or illness."
            },
            
            {
                "name": "Irritable Bowel Syndrome",
                "overview": "Irritable Bowel Syndrome (IBS) is a chronic gastrointestinal disorder affecting bowel function. It causes abdominal pain and changes in bowel habits without causing permanent damage to the intestines. IBS affects the large intestine and is a functional disorder rather than a structural disease.",
                "symptoms": "Abdominal pain and cramping (usually in lower abdomen); Bloating and gas; Diarrhea, constipation, or alternating between both; Mucus in stool; Feeling of incomplete bowel movements; Urgency or frequency changes; Symptoms often triggered by stress or certain foods",
                "causes": "Exact cause unknown; Abnormal gut-brain communication; Increased sensitivity to pain in digestive tract; Post-infectious changes after gastroenteritis; Food intolerances (dairy, gluten, FODMAPs); Stress and anxiety; Hormonal changes; Small intestinal bacterial overgrowth (SIBO)",
                "treatments": "Dietary modifications (low-FODMAP diet, fiber adjustment); Stress management techniques; Probiotics; Antispasmodic medications; Anti-diarrheal or laxative medications as needed; Psychological therapy (cognitive behavioral therapy); Regular exercise; Adequate sleep",
                "when_to_see_doctor": "Unexplained weight loss; Blood in stool; Severe abdominal pain; Persistent symptoms interfering with daily life; Symptoms beginning after age 50; Family history of colorectal cancer or inflammatory bowel disease; Night-time symptoms disrupting sleep",
                "prevention": "Identify and avoid trigger foods; Manage stress through relaxation techniques; Maintain regular eating schedule; Stay hydrated; Exercise regularly; Get adequate sleep; Consider probiotic foods; Limit caffeine and alcohol",
                "how_common": "Very common - affects 10-15% of the global population. More common in women than men (2:1 ratio). Often begins in late teens to early 40s. Many people have mild symptoms that don't require medical treatment."
            },
            
            {
                "name": "Food Intolerance",
                "overview": "Food intolerance occurs when the digestive system has difficulty processing certain foods or food components. Unlike food allergies, which involve the immune system, food intolerances are digestive issues that typically cause discomfort but are not life-threatening.",
                "symptoms": "Bloating and abdominal distension; Gas and flatulence; Stomach pain or cramping; Diarrhea or loose stools; Nausea; Headaches; Fatigue after eating; Skin irritation (occasionally); Heartburn or acid reflux",
                "causes": "Lactose intolerance (inability to digest milk sugar); Fructose malabsorption; Gluten sensitivity; Food additives (sulfites, MSG, artificial colors); Enzyme deficiencies; High-FODMAP foods; Caffeine sensitivity; Histamine intolerance",
                "treatments": "Elimination diet to identify trigger foods; Food diary tracking; Enzyme supplements (lactase for dairy); Gradual reintroduction of tolerated amounts; Digestive aids; Probiotics; Small, frequent meals; Reading food labels carefully",
                "when_to_see_doctor": "Severe or persistent digestive symptoms; Unexplained weight loss; Blood in stool; Symptoms that interfere with daily activities; Suspicion of celiac disease or other serious conditions; Need for professional dietary guidance",
                "prevention": "Identify personal trigger foods through systematic elimination; Read ingredient labels carefully; Choose fresh, unprocessed foods when possible; Take enzyme supplements as recommended; Eat smaller portions of problematic foods; Prepare meals at home when possible",
                "how_common": "Very common - affects up to 20% of the population. Lactose intolerance affects 65% of adults worldwide. Prevalence varies by ethnicity and geographic region. Often develops or worsens with age."
            },
            
            {
                "name": "Functional Dyspepsia",
                "overview": "Functional dyspepsia, also known as non-ulcer dyspepsia, is chronic or recurring indigestion without an identifiable structural cause. It involves symptoms of upper abdominal discomfort that persist despite normal test results for ulcers or other digestive conditions.",
                "symptoms": "Upper abdominal pain or discomfort; Early satiety (feeling full quickly); Postprandial fullness (prolonged fullness after meals); Bloating and abdominal distension; Nausea; Heartburn or burning sensation; Belching; Loss of appetite",
                "causes": "Delayed gastric emptying; Abnormal gastric muscle function; Increased sensitivity to stomach acid; H. pylori bacterial infection (in some cases); Stress and psychological factors; Certain medications; Smoking and alcohol consumption",
                "treatments": "Acid-reducing medications (proton pump inhibitors, H2 blockers); H. pylori treatment if infection present; Prokinetic agents to improve stomach emptying; Dietary modifications (smaller, frequent meals); Stress management; Antidepressants for severe cases; Lifestyle changes",
                "when_to_see_doctor": "Persistent symptoms lasting more than 4 weeks; Unexplained weight loss; Difficulty swallowing; Vomiting blood or coffee-ground material; Black, tarry stools; Severe or worsening pain; Family history of stomach cancer",
                "prevention": "Eat smaller, more frequent meals; Avoid trigger foods (spicy, fatty, acidic foods); Limit alcohol and quit smoking; Manage stress through relaxation techniques; Maintain healthy weight; Avoid medications that irritate the stomach; Regular meal times",
                "how_common": "Common - affects 10-15% of the population. More prevalent in women than men. Often begins in young adulthood. Many people experience occasional symptoms, but chronic cases require medical evaluation."
            },

            # RESPIRATORY DISEASES
            {
                "name": "Upper Respiratory Infection",
                "overview": "Upper Respiratory Infection (URI) is a common viral infection affecting the nose, throat, pharynx, and larynx. Also known as the common cold, it typically resolves on its own within 7-10 days and rarely causes serious complications in healthy individuals.",
                "symptoms": "Runny or stuffy nose; Sneezing; Sore throat; Mild cough; Low-grade fever; Headache; Fatigue; Body aches; Hoarseness; Post-nasal drip; Watery eyes",
                "causes": "Viral infections (rhinoviruses most common, also coronaviruses, adenoviruses, RSV); Spread through respiratory droplets; Direct contact with contaminated surfaces; Close contact with infected individuals; Weakened immune system",
                "treatments": "Rest and adequate sleep; Increased fluid intake; Humidified air or steam inhalation; Salt water gargles; Over-the-counter pain relievers and decongestants; Throat lozenges; Avoid smoking and irritants; Honey for cough relief",
                "when_to_see_doctor": "Fever above 38.5°C (101.3°F) lasting more than 3 days; Difficulty breathing or wheezing; Severe headache or sinus pain; Thick, colored nasal discharge persisting beyond 10 days; Ear pain; Worsening symptoms after initial improvement",
                "prevention": "Frequent handwashing with soap; Avoid touching face with unwashed hands; Avoid close contact with sick individuals; Cover coughs and sneezes; Disinfect frequently touched surfaces; Maintain healthy lifestyle; Get adequate sleep",
                "how_common": "Very common - adults average 2-3 colds per year, children 6-8 per year. Most frequent during fall and winter months. Nearly everyone experiences URIs regularly throughout their lifetime."
            },
            
            {
                "name": "Common Cold",
                "overview": "The common cold is a mild viral infection of the upper respiratory tract, primarily affecting the nose and throat. It is one of the most frequent illnesses in humans and typically resolves without treatment within a week to ten days.",
                "symptoms": "Runny or congested nose; Sneezing; Sore or scratchy throat; Mild cough; Low-grade fever (more common in children); Headache; Body aches; Fatigue; Watery eyes; Post-nasal drip",
                "causes": "Viral infections (rhinoviruses cause 30-50% of colds); Transmitted through airborne droplets; Contact with contaminated surfaces; Hand-to-hand contact; More common in cold weather when people gather indoors",
                "treatments": "Rest and increased fluid intake; Over-the-counter medications for symptom relief; Warm salt water gargles; Humidified air; Throat lozenges; Avoid unnecessary antibiotics; Gradual return to normal activities as symptoms improve",
                "when_to_see_doctor": "Fever above 38.5°C (101.3°F) lasting more than 3 days; Symptoms lasting more than 10 days; Difficulty breathing; Severe headache; Ear pain or discharge; Worsening symptoms instead of gradual improvement",
                "prevention": "Regular handwashing for at least 20 seconds; Avoid touching eyes, nose, and mouth; Keep distance from sick individuals; Clean and disinfect shared surfaces; Maintain good hygiene; Support immune system with proper nutrition and sleep",
                "how_common": "Extremely common - most frequent infectious disease in humans. Adults typically get 2-4 colds per year, children 6-10 per year. Accounts for millions of doctor visits and missed work/school days annually."
            },
            
            {
                "name": "Viral Pharyngitis",
                "overview": "Viral pharyngitis is inflammation of the pharynx (throat) caused by viral infections. It commonly accompanies upper respiratory infections and is characterized by throat pain and irritation that typically resolves within 3-7 days.",
                "symptoms": "Sore throat (ranging from mild to severe); Scratchy or dry throat sensation; Pain when swallowing; Red and swollen throat; Mild fever; Fatigue; Headache; Swollen lymph nodes; Hoarseness; Runny nose and cough (if part of URI)",
                "causes": "Viral infections (rhinoviruses, adenoviruses, influenza viruses, Epstein-Barr virus); Spread through respiratory droplets; Direct contact with infected saliva; Touching contaminated surfaces then touching mouth or nose",
                "treatments": "Rest and voice conservation; Increased fluid intake (warm liquids preferred); Warm salt water gargles; Throat lozenges or sprays; Over-the-counter pain relievers; Humidified air; Avoid irritants like smoke; Cool or soft foods",
                "when_to_see_doctor": "Severe throat pain preventing swallowing; High fever above 38.5°C (101.3°F); White patches or pus on tonsils; Difficulty breathing or opening mouth; Persistent symptoms beyond 7 days; Swollen lymph nodes with fever",
                "prevention": "Frequent handwashing; Avoid sharing eating utensils or drinks; Cover mouth when coughing or sneezing; Avoid close contact with infected individuals; Maintain good oral hygiene; Support immune system with adequate rest",
                "how_common": "Very common - most sore throats are viral in origin. Accounts for approximately 85% of pharyngitis cases. More frequent during fall and winter months. Often occurs as part of broader respiratory infections."
            },
            
            {
                "name": "Allergic Rhinitis",
                "overview": "Allergic rhinitis, commonly known as hay fever, is an allergic reaction that causes inflammation of the nasal passages. It occurs when the immune system overreacts to airborne allergens, leading to nasal and respiratory symptoms.",
                "symptoms": "Sneezing (often in fits); Runny nose with clear discharge; Nasal congestion; Itchy nose, eyes, or throat; Watery, red eyes; Post-nasal drip; Cough; Fatigue; Dark circles under eyes; Decreased sense of smell",
                "causes": "Outdoor allergens (tree, grass, and weed pollens); Indoor allergens (dust mites, pet dander, mold, cockroaches); Occupational allergens; Genetic predisposition; Environmental factors; Cross-reactivity with foods",
                "treatments": "Antihistamines (oral, nasal, or eye drops); Nasal corticosteroid sprays; Decongestants (short-term use); Saline nasal rinses; Allergen immunotherapy (allergy shots or tablets); Mast cell stabilizers; Environmental control measures",
                "when_to_see_doctor": "Symptoms significantly interfering with daily activities; Poor response to over-the-counter medications; Chronic sinus infections; Asthma symptoms; Sleep disturbances; Need for allergy testing and specific treatment plans",
                "prevention": "Identify and avoid specific allergens; Keep windows closed during high pollen seasons; Use air purifiers with HEPA filters; Wash bedding in hot water weekly; Remove carpets and minimize indoor plants; Shower after outdoor activities",
                "how_common": "Very common - affects 10-30% of adults and up to 40% of children globally. Prevalence increasing in developed countries. Often begins in childhood and may persist throughout life. Strong genetic component."
            },
            
            {
                "name": "Throat Irritation",
                "overview": "Throat irritation refers to discomfort, scratchiness, or mild pain in the throat that can be caused by various environmental, infectious, or behavioral factors. It is typically a temporary condition that resolves once the underlying cause is addressed.",
                "symptoms": "Scratchy or dry throat sensation; Mild throat pain; Tickling sensation causing frequent coughing; Hoarseness; Feeling of something stuck in throat; Mild difficulty swallowing; Throat clearing; Irritating cough",
                "causes": "Environmental irritants (smoke, pollution, dry air); Viral infections; Allergic reactions; Acid reflux (GERD); Voice overuse or strain; Mouth breathing; Certain medications; Dehydration; Chemical exposures",
                "treatments": "Stay hydrated with warm liquids; Use humidifier or breathe steam; Throat lozenges or hard candies; Warm salt water gargles; Rest voice; Avoid irritants; Over-the-counter pain relievers if needed; Address underlying causes",
                "when_to_see_doctor": "Persistent irritation lasting more than 7-10 days; Severe pain or difficulty swallowing; Fever accompanying throat symptoms; Voice changes lasting more than 2 weeks; Breathing difficulties; Blood in saliva",
                "prevention": "Avoid smoking and secondhand smoke; Use humidifier in dry environments; Stay hydrated; Practice good vocal hygiene; Manage acid reflux; Avoid known allergens; Limit exposure to environmental irritants",
                "how_common": "Very common - most people experience throat irritation periodically. Often occurs seasonally due to allergens or dry air. Frequently associated with upper respiratory infections or environmental exposures."
            },

            # HEADACHE/PAIN DISEASES
            {
                "name": "Tension Headache",
                "overview": "Tension headaches are the most common type of headache, characterized by mild to moderate pain that feels like pressure or tightness around the head. They are often related to stress, muscle tension, or fatigue and typically respond well to simple treatments.",
                "symptoms": "Dull, aching head pain; Sensation of tight band around head; Pressure across forehead or back of head; Tenderness in scalp, neck, and shoulder muscles; Bilateral pain (both sides of head); No nausea or vomiting typically",
                "causes": "Stress and anxiety; Muscle tension in neck and shoulders; Poor posture; Eye strain; Fatigue and sleep deprivation; Dehydration; Irregular meals; Hormone fluctuations; Environmental factors",
                "treatments": "Over-the-counter pain relievers (acetaminophen, ibuprofen, aspirin); Rest in quiet, dark room; Stress management techniques; Neck and shoulder massage; Hot or cold compresses; Regular sleep schedule; Relaxation exercises",
                "when_to_see_doctor": "Sudden severe headache unlike previous ones; Headaches with fever, stiff neck, or rash; Progressive worsening of headache pattern; Headaches after head injury; Vision changes or weakness; Headaches interfering with daily life",
                "prevention": "Manage stress effectively; Maintain regular sleep schedule; Stay hydrated; Eat regular meals; Practice good posture; Take breaks from computer work; Regular exercise; Limit caffeine; Identify and avoid triggers",
                "how_common": "Very common - affects up to 80% of adults occasionally. More frequent in women than men. Most people experience tension headaches at some point. Often begins in teenage years and may continue throughout life."
            },
            
            {
                "name": "Migraine",
                "overview": "Migraine is a neurological disorder characterized by recurrent, severe headaches often accompanied by nausea, vomiting, and sensitivity to light and sound. It can significantly impact quality of life and daily functioning.",
                "symptoms": "Severe, throbbing headache (usually one-sided); Nausea and vomiting; Sensitivity to light and sound; Visual disturbances (aura in some people); Dizziness; Fatigue; Difficulty concentrating; Neck stiffness; Mood changes",
                "causes": "Genetic predisposition; Hormonal changes; Certain foods and drinks; Stress; Sleep changes; Environmental factors; Bright lights or loud sounds; Strong smells; Weather changes; Certain medications",
                "treatments": "Prescription medications (triptans, ergots); Over-the-counter pain relievers; Anti-nausea medications; Rest in dark, quiet room; Cold compresses; Preventive medications for frequent migraines; Lifestyle modifications; Trigger avoidance",
                "when_to_see_doctor": "Frequent migraines (more than 4 per month); Sudden severe headache; Headache with fever and stiff neck; Changes in headache pattern; Headache after head injury; Aura lasting more than an hour; Weakness or speech problems",
                "prevention": "Identify and avoid triggers; Maintain regular sleep schedule; Manage stress; Stay hydrated; Eat regular meals; Limit caffeine; Exercise regularly; Consider preventive medications; Keep headache diary",
                "how_common": "Common - affects about 12% of the population. Three times more common in women than men. Often begins in adolescence and peaks during middle age. Strong genetic component with family history."
            },
            
            {
                "name": "Stress Headache",
                "overview": "Stress headaches are tension-type headaches specifically triggered by emotional or physical stress. They result from muscle contractions in the head and neck area due to stress responses and are among the most treatable types of headaches.",
                "symptoms": "Mild to moderate constant aching; Feeling of pressure or tightness; Usually affects both sides of head; Neck and shoulder muscle tension; May worsen with stress; No nausea or vomiting typically; Gradual onset",
                "causes": "Emotional stress; Work pressure; Relationship problems; Financial worries; Major life changes; Physical stress; Lack of relaxation; Anxiety and depression; Poor stress management skills",
                "treatments": "Stress management techniques; Relaxation exercises (deep breathing, meditation); Regular exercise; Adequate sleep; Massage therapy; Yoga or tai chi; Over-the-counter pain relievers; Counseling if needed",
                "when_to_see_doctor": "Frequent stress headaches interfering with daily life; Inability to manage stress effectively; Headaches accompanied by anxiety or depression; Need for stress management strategies; Medication overuse concerns",
                "prevention": "Learn effective stress management techniques; Practice regular relaxation; Maintain work-life balance; Exercise regularly; Get adequate sleep; Build strong support network; Seek counseling for chronic stress; Time management skills",
                "how_common": "Very common - stress is one of the most frequent headache triggers. Nearly everyone experiences stress-related headaches occasionally. More prevalent during high-stress life periods. Often improves with stress management."
            },
            
            {
                "name": "Muscle Strain",
                "overview": "Muscle strain, commonly called a pulled muscle, occurs when muscle fibers are overstretched or torn. It can affect any muscle but commonly occurs in the back, neck, shoulder, and leg muscles during physical activity or sudden movements.",
                "symptoms": "Sudden pain during muscle use; Muscle spasms; Swelling and tenderness; Limited range of motion; Muscle weakness; Bruising (in severe cases); Stiffness; Pain that worsens with movement",
                "causes": "Overexertion during exercise; Improper lifting techniques; Poor flexibility; Sudden movements; Muscle fatigue; Inadequate warm-up; Previous muscle injuries; Poor conditioning; Repetitive motions",
                "treatments": "Rest and avoid aggravating activities; Ice application (first 48 hours); Compression with elastic bandage; Elevation when possible; Over-the-counter pain relievers; Gentle stretching; Physical therapy; Gradual return to activity",
                "when_to_see_doctor": "Severe pain or inability to use the muscle; Numbness or tingling; Signs of infection; No improvement after several days; Recurrent muscle strains; Inability to walk or bear weight",
                "prevention": "Proper warm-up before exercise; Regular stretching; Gradual increase in activity intensity; Proper lifting techniques; Adequate rest between workouts; Maintain good physical conditioning; Stay hydrated; Use proper equipment",
                "how_common": "Very common - affects most people at some point. More frequent in athletes and physically active individuals. Risk increases with age due to decreased flexibility. Often occurs during sports or exercise activities."
            },
            
            {
                "name": "Arthralgia",
                "overview": "Arthralgia refers to joint pain without inflammation. It is a symptom rather than a diagnosis and can affect one or multiple joints. The pain may be acute or chronic and can significantly impact mobility and quality of life.",
                "symptoms": "Joint pain (sharp, dull, throbbing, or burning); Stiffness in affected joints; Reduced range of motion; Tenderness when joint is touched; Pain that may worsen with movement; Morning stiffness; Aching sensation",
                "causes": "Overuse or repetitive motion; Minor injuries; Viral infections; Medication side effects; Autoimmune conditions; Age-related wear and tear; Weather changes; Previous joint injuries; Inflammatory conditions",
                "treatments": "Rest and joint protection; Over-the-counter pain relievers; Hot or cold therapy; Gentle exercise and stretching; Physical therapy; Weight management; Supportive devices (braces, splints); Address underlying causes",
                "when_to_see_doctor": "Persistent pain lasting more than a few days; Severe or worsening pain; Joint swelling, redness, or warmth; Pain after injury; Fever with joint pain; Inability to use the joint normally",
                "prevention": "Regular low-impact exercise; Maintain healthy weight; Use proper body mechanics; Take breaks during repetitive activities; Stay hydrated; Wear supportive footwear; Protect joints during activities",
                "how_common": "Very common - joint pain affects most adults at some point. Increases with age due to normal wear and tear. Can occur at any age depending on underlying cause. Often temporary and resolves with appropriate care."
            },
            
            {
                "name": "Inflammatory Pain",
                "overview": "Inflammatory pain arises when the body's immune response to injury or irritation causes inflammation, resulting in pain and hypersensitivity. It serves as a protective mechanism but can become problematic when chronic or excessive.",
                "symptoms": "Persistent or throbbing pain; Redness and warmth at affected site; Swelling and tenderness; Stiffness, especially after rest; Loss of function; Pain that may worsen at night; Fatigue; Low-grade fever (sometimes)",
                "causes": "Autoimmune diseases; Infections; Physical injuries; Chronic inflammatory conditions; Certain medications; Environmental toxins; Stress; Poor diet; Lack of exercise; Age-related changes",
                "treatments": "Anti-inflammatory medications (NSAIDs); Corticosteroids for severe cases; Physical therapy; Regular exercise; Anti-inflammatory diet; Stress management; Hot/cold therapy; Massage; Rest and adequate sleep",
                "when_to_see_doctor": "Persistent pain not responding to over-the-counter medications; Swelling and warmth in joints or muscles; Fever with pain; Unexplained weight loss; Pain interfering with daily activities; Progressive worsening",
                "prevention": "Anti-inflammatory diet rich in omega-3 fatty acids; Regular physical activity; Maintain healthy weight; Manage stress effectively; Avoid smoking; Limit alcohol; Get adequate sleep; Stay hydrated",
                "how_common": "Common - inflammatory conditions affect millions worldwide. Prevalence increases with age. Women are more commonly affected by certain inflammatory conditions. Early intervention can prevent chronic inflammation."
            },

            # VIRAL/FEVER DISEASES
            {
                "name": "Viral Infection",
                "overview": "A viral infection occurs when viruses invade the body's cells and multiply, causing illness. Viruses can affect various body systems and cause a wide range of symptoms. Unlike bacterial infections, viral infections do not respond to antibiotics.",
                "symptoms": "Fever; Fatigue and weakness; Body aches and pains; Headache; Cough; Sore throat; Runny or stuffy nose; Nausea; Diarrhea; Skin rash (sometimes); Swollen lymph nodes",
                "causes": "Various viruses (rhinoviruses, influenza, coronaviruses, adenoviruses); Transmitted through respiratory droplets; Direct contact; Contaminated surfaces; Airborne transmission; Vector-borne transmission",
                "treatments": "Rest and adequate sleep; Increased fluid intake; Over-the-counter medications for symptom relief; Antiviral medications (for specific infections); Supportive care; Symptomatic treatment; Allow immune system to fight infection",
                "when_to_see_doctor": "High fever above 39°C (102°F); Difficulty breathing; Persistent vomiting; Signs of dehydration; Symptoms lasting more than 10 days; Worsening symptoms; Severe fatigue or weakness",
                "prevention": "Frequent handwashing; Avoid close contact with sick individuals; Cover coughs and sneezes; Disinfect surfaces; Stay up-to-date with vaccinations; Maintain good hygiene; Support immune system with healthy lifestyle",
                "how_common": "Very common - viral infections are among the most frequent illnesses. Most people experience several viral infections each year. More common during fall and winter months. Usually mild and self-limiting."
            },
            
            {
                "name": "Influenza",
                "overview": "Influenza, commonly called the flu, is a contagious respiratory illness caused by influenza viruses. It typically occurs seasonally and can range from mild to severe illness, sometimes leading to hospitalization or death in vulnerable populations.",
                "symptoms": "Sudden onset of fever; Chills and sweats; Severe body aches; Headache; Dry cough; Fatigue and weakness; Sore throat; Runny or stuffy nose; Nausea and vomiting (more common in children)",
                "causes": "Influenza A and B viruses; Transmitted through respiratory droplets; Person-to-person contact; Contaminated surfaces; Seasonal epidemics; Antigenic drift and shift of virus strains",
                "treatments": "Rest and increased fluid intake; Antiviral medications (most effective within 48 hours); Over-the-counter medications for symptom relief; Avoid aspirin in children; Symptomatic treatment; Gradual return to activities",
                "when_to_see_doctor": "Difficulty breathing; Chest pain; Persistent dizziness; Severe or persistent vomiting; High-risk individuals (elderly, pregnant, chronic conditions); Symptoms that improve then worsen; Signs of secondary infection",
                "prevention": "Annual flu vaccination; Frequent handwashing; Avoid touching face; Cover coughs and sneezes; Avoid close contact with sick people; Stay home when sick; Disinfect surfaces; Maintain healthy lifestyle",
                "how_common": "Common - affects 5-20% of the population annually. Seasonal epidemics occur yearly, typically in fall and winter. Vaccination reduces risk by 40-60% when well-matched to circulating strains."
            },
            
            {
                "name": "Mild Viral Infection",
                "overview": "Mild viral infections are common, self-limiting illnesses caused by various viruses. They typically cause temporary discomfort and resolve within a few days to a week without requiring medical intervention or causing serious complications.",
                "symptoms": "Low-grade fever; Mild fatigue; Runny nose; Mild cough; Sore throat; Headache; Minor body aches; Reduced appetite; Mild nausea; General malaise",
                "causes": "Common viruses (rhinoviruses, coronaviruses, adenoviruses); Respiratory transmission; Contact with contaminated surfaces; Seasonal viral circulation; Person-to-person contact",
                "treatments": "Rest and adequate sleep; Increased fluid intake; Over-the-counter symptom relief; Warm salt water gargles; Humidified air; Avoid unnecessary antibiotics; Monitor symptoms; Gradual activity resumption",
                "when_to_see_doctor": "Symptoms persisting beyond 10 days; High fever; Difficulty breathing; Severe headache; Signs of bacterial secondary infection; Worsening rather than improving symptoms",
                "prevention": "Good hand hygiene; Avoid close contact with sick individuals; Cover coughs and sneezes; Disinfect frequently touched surfaces; Maintain healthy immune system; Get adequate rest",
                "how_common": "Very common - most people experience several mild viral infections yearly. Peak incidence during colder months. Generally benign and resolve without complications in healthy individuals."
            },
            
            {
                "name": "Bacterial Infection",
                "overview": "Bacterial infections occur when harmful bacteria multiply in the body, causing illness. Unlike viral infections, bacterial infections can be treated with antibiotics and may cause more serious complications if left untreated.",
                "symptoms": "Fever (often higher than viral infections); Localized pain and swelling; Pus or discharge; Redness and warmth; Fatigue; Chills; Specific symptoms depending on location (respiratory, urinary, skin, etc.)",
                "causes": "Various bacteria (Streptococcus, Staphylococcus, E. coli, etc.); Breaks in skin; Contaminated food or water; Person-to-person transmission; Medical procedures; Weakened immune system",
                "treatments": "Prescription antibiotics (specific to bacteria type); Complete full antibiotic course; Supportive care; Pain management; Rest and hydration; Drainage of abscesses if needed; Follow-up care",
                "when_to_see_doctor": "Suspected bacterial infection; High fever; Severe or worsening symptoms; Pus or unusual discharge; Red streaking from infection site; Signs of sepsis; Failed response to initial treatment",
                "prevention": "Proper wound care; Good hygiene practices; Safe food handling; Complete antibiotic courses as prescribed; Vaccinations; Avoid sharing personal items; Hand washing",
                "how_common": "Common but less frequent than viral infections. Can be serious if untreated. Response to appropriate antibiotics is usually good. Prevention through hygiene and vaccination is effective."
            },
            
            # SKIN/ALLERGIC DISEASES
            {
                "name": "Contact Dermatitis",
                "overview": "Contact dermatitis is a skin inflammation caused by direct contact with an irritating substance or allergen. It results in red, itchy, and sometimes painful skin that can develop blisters or scaling depending on the severity of the reaction.",
                "symptoms": "Red, inflamed skin; Itching and burning sensation; Swelling; Blisters or bumps; Dry, cracked, or scaly skin; Tenderness or pain; Skin that feels warm to touch; In severe cases, oozing or crusting",
                "causes": "Irritant contact dermatitis from chemicals, soaps, detergents; Allergic contact dermatitis from metals (nickel), plants (poison ivy), cosmetics, fragrances; Latex or rubber exposure; Certain fabrics or dyes; Prolonged moisture exposure",
                "treatments": "Remove or avoid the irritant/allergen; Cool, wet compresses; Topical corticosteroid creams; Oral antihistamines for itching; Moisturizers to restore skin barrier; Oral corticosteroids for severe cases; Avoid scratching to prevent infection",
                "when_to_see_doctor": "Severe or widespread rash; Signs of infection (pus, increased redness, warmth); Rash doesn't improve after 2-3 weeks; Difficulty identifying the cause; Rash affects face, genitals, or large body areas; Fever with skin symptoms",
                "prevention": "Identify and avoid known triggers; Use protective equipment when handling chemicals; Choose hypoallergenic products; Moisturize skin regularly; Patch test new products; Wear appropriate clothing; Keep skin clean and dry",
                "how_common": "Very common - affects most people at some point. Contact dermatitis accounts for 95% of occupational skin diseases. More frequent in people with sensitive skin or those exposed to chemicals regularly."
            },
            
            {
                "name": "Allergic Reaction",
                "overview": "An allergic reaction occurs when the immune system overreacts to a normally harmless substance (allergen). Reactions can range from mild skin irritation to severe, life-threatening anaphylaxis, depending on the individual's sensitivity and the type of exposure.",
                "symptoms": "Skin reactions (hives, rash, itching, swelling); Respiratory symptoms (sneezing, coughing, wheezing, shortness of breath); Digestive issues (nausea, vomiting, diarrhea, cramping); Swelling of face, lips, tongue, or throat; Rapid pulse; Dizziness or fainting",
                "causes": "Food allergens (nuts, shellfish, eggs, dairy); Environmental allergens (pollen, dust mites, pet dander); Medications (antibiotics, aspirin); Insect stings or bites; Latex; Chemical exposure; Cross-reactivity between allergens",
                "treatments": "Remove or avoid the allergen; Antihistamines for mild reactions; Topical corticosteroids for skin symptoms; Epinephrine auto-injector for severe reactions; Bronchodilators for breathing difficulties; Emergency medical care for anaphylaxis",
                "when_to_see_doctor": "Severe or widespread symptoms; Difficulty breathing or swallowing; Rapid pulse or dizziness; Previous severe allergic reactions; Unknown cause of reaction; Symptoms not improving with treatment; Need for allergy testing",
                "prevention": "Identify and avoid known allergens; Read food and product labels carefully; Carry epinephrine auto-injector if prescribed; Wear medical alert jewelry; Inform healthcare providers of allergies; Consider allergy immunotherapy",
                "how_common": "Very common - affects up to 50 million Americans. Food allergies affect 4-6% of children and 4% of adults. Environmental allergies are even more prevalent. Severe reactions are less common but can be life-threatening."
            },
            
            {
                "name": "Eczema",
                "overview": "Eczema, also known as atopic dermatitis, is a chronic inflammatory skin condition characterized by itchy, red, and inflamed patches of skin. It often begins in childhood and can persist into adulthood, with symptoms that flare up periodically.",
                "symptoms": "Itchy, red, or brownish-gray patches; Small, raised bumps that may leak fluid when scratched; Thickened, cracked, or scaly skin; Raw, sensitive skin from scratching; Dry skin; Sleep disturbances due to itching",
                "causes": "Genetic predisposition; Immune system dysfunction; Environmental triggers (allergens, irritants); Stress; Weather changes; Certain foods; Hormonal changes; Bacterial or viral infections",
                "treatments": "Moisturize regularly with fragrance-free products; Topical corticosteroids during flare-ups; Topical calcineurin inhibitors; Antihistamines for itching; Avoid known triggers; Cool baths with oatmeal or baking soda; Prescription medications for severe cases",
                "when_to_see_doctor": "Severe or worsening symptoms; Signs of infection (pus, fever, red streaks); Eczema interfering with sleep or daily activities; No improvement with over-the-counter treatments; Need for prescription medications or allergy testing",
                "prevention": "Moisturize skin daily; Use mild, fragrance-free soaps and detergents; Avoid known triggers; Manage stress; Maintain comfortable humidity levels; Wear soft, breathable fabrics; Keep fingernails short to prevent scratching damage",
                "how_common": "Very common - affects 10-20% of children and 1-3% of adults worldwide. Often begins in early childhood, with many children outgrowing it by adolescence. Strong genetic component with family history of allergies or asthma."
            },
            
            # NEUROLOGICAL/BALANCE DISEASES
            {
                "name": "Vertigo",
                "overview": "Vertigo is a sensation of spinning or movement when you are actually stationary. It is often caused by problems in the inner ear or brain and can be accompanied by nausea, vomiting, and balance difficulties. Episodes can last from minutes to hours.",
                "symptoms": "Spinning sensation (feeling like you or surroundings are moving); Nausea and vomiting; Balance problems and unsteadiness; Headache; Sweating; Hearing loss or ringing in ears (sometimes); Jerking eye movements (nystagmus)",
                "causes": "Benign paroxysmal positional vertigo (BPPV); Vestibular neuritis; Meniere's disease; Labyrinthitis; Migraines; Head or neck injury; Certain medications; Acoustic neuroma (rare); Central nervous system disorders",
                "treatments": "Canalith repositioning procedures (Epley maneuver); Vestibular rehabilitation exercises; Medications for nausea and dizziness; Balance training; Lifestyle modifications; Treatment of underlying conditions; Surgery in rare cases",
                "when_to_see_doctor": "Severe or persistent vertigo; Vertigo with hearing loss; High fever with vertigo; Severe headache; Weakness or numbness; Speech or vision problems; Vertigo after head injury; Symptoms interfering with daily life",
                "prevention": "Avoid sudden head movements; Move slowly when changing positions; Stay hydrated; Manage stress; Avoid triggers if known; Regular exercise to maintain balance; Protect head from injury; Limit alcohol consumption",
                "how_common": "Common - affects about 40% of people over age 40 at least once. BPPV is the most common cause. More frequent in women than men. Often recurrent but usually treatable with proper management."
            },
            
            {
                "name": "Inner Ear Disorder",
                "overview": "Inner ear disorders affect the delicate structures responsible for hearing and balance. These conditions can cause dizziness, hearing loss, and balance problems, significantly impacting daily activities and quality of life.",
                "symptoms": "Dizziness or vertigo; Hearing loss or changes; Tinnitus (ringing in ears); Balance problems; Nausea and vomiting; Feeling of fullness in ear; Unsteadiness when walking; Sensitivity to loud sounds",
                "causes": "Viral or bacterial infections; Age-related changes; Head trauma; Meniere's disease; Acoustic neuroma; Ototoxic medications; Autoimmune conditions; Genetic factors; Circulation problems",
                "treatments": "Medications for symptoms (anti-nausea, diuretics); Vestibular rehabilitation therapy; Hearing aids if needed; Lifestyle modifications; Stress management; Avoid triggers; Surgical intervention in severe cases; Balance training exercises",
                "when_to_see_doctor": "Sudden hearing loss; Severe or persistent dizziness; Hearing loss with pain; Discharge from ear; Symptoms after head injury; Progressive hearing loss; Balance problems affecting daily life; Severe tinnitus",
                "prevention": "Protect ears from loud noises; Avoid ototoxic medications when possible; Treat ear infections promptly; Maintain good hygiene; Avoid inserting objects in ears; Manage blood pressure and diabetes; Regular hearing check-ups",
                "how_common": "Common - inner ear problems affect millions of people. Hearing loss affects 1 in 8 Americans. Balance disorders affect 35% of adults over 70. Many conditions are age-related but can occur at any age."
            },
            
            {
                "name": "Vestibular Dysfunction",
                "overview": "Vestibular dysfunction refers to problems with the vestibular system in the inner ear that controls balance and spatial orientation. It can cause dizziness, imbalance, and difficulty with coordination and movement.",
                "symptoms": "Dizziness and unsteadiness; Balance problems; Nausea and vomiting; Visual disturbances; Difficulty concentrating; Fatigue; Anxiety about falling; Disorientation; Motion sensitivity",
                "causes": "Vestibular neuritis; Labyrinthitis; BPPV; Meniere's disease; Head trauma; Viral infections; Age-related changes; Medications; Migraines; Central nervous system disorders",
                "treatments": "Vestibular rehabilitation therapy; Medications for symptom control; Balance and gait training; Canalith repositioning maneuvers; Lifestyle modifications; Stress management; Fall prevention strategies; Treatment of underlying causes",
                "when_to_see_doctor": "Persistent or severe dizziness; Balance problems affecting daily activities; Falls or near-falls; Hearing changes with dizziness; Severe headache with balance problems; Symptoms after head injury; Progressive worsening",
                "prevention": "Regular exercise to maintain balance; Home safety modifications; Avoid sudden movements; Stay hydrated; Manage medications carefully; Protect head from injury; Regular check-ups for underlying conditions",
                "how_common": "Common - vestibular disorders affect 35% of adults over 40. More frequent with advancing age. Can significantly impact quality of life but often responds well to appropriate treatment and rehabilitation."
            },
            
            # FATIGUE/GENERAL DISEASES
            {
                "name": "Chronic Fatigue",
                "overview": "Chronic fatigue is persistent, unexplained exhaustion that lasts for six months or longer and doesn't improve with rest. It significantly impacts daily functioning and may be accompanied by other symptoms affecting multiple body systems.",
                "symptoms": "Severe fatigue not relieved by rest; Post-exertional malaise; Sleep problems; Cognitive difficulties (brain fog); Muscle and joint pain; Headaches; Sore throat; Tender lymph nodes; Orthostatic intolerance",
                "causes": "Unknown exact cause; Possible viral infections; Immune system dysfunction; Stress; Genetic predisposition; Hormonal imbalances; Environmental factors; Sleep disorders; Depression or anxiety",
                "treatments": "Pacing and energy management; Graded exercise therapy (controversial); Cognitive behavioral therapy; Sleep hygiene; Stress management; Symptom-specific medications; Nutritional support; Activity modification",
                "when_to_see_doctor": "Fatigue lasting more than 6 months; Severe functional impairment; Other unexplained symptoms; Sleep disturbances; Cognitive problems; Depression or anxiety; Need for comprehensive evaluation and management plan",
                "prevention": "Maintain good sleep hygiene; Manage stress effectively; Eat balanced diet; Exercise regularly (within limits); Avoid overexertion; Treat underlying conditions; Maintain social connections; Pace activities appropriately",
                "how_common": "Affects 836,000 to 2.5 million Americans. More common in women than men (3:1 ratio). Can occur at any age but peaks in 40s and 50s. Often misdiagnosed or unrecognized."
            },
            
            {
                "name": "Sleep Disorder",
                "overview": "Sleep disorders are conditions that affect the quality, timing, and amount of sleep, resulting in daytime distress and impairment in functioning. They can significantly impact physical health, mental health, and quality of life.",
                "symptoms": "Difficulty falling or staying asleep; Excessive daytime sleepiness; Loud snoring or breathing interruptions; Unrefreshing sleep; Restless legs; Sleepwalking or night terrors; Irregular sleep-wake patterns; Morning headaches",
                "causes": "Sleep apnea; Insomnia; Stress and anxiety; Medical conditions; Medications; Caffeine or alcohol; Poor sleep hygiene; Shift work; Aging; Mental health disorders; Neurological conditions",
                "treatments": "Sleep hygiene education; Continuous positive airway pressure (CPAP) for sleep apnea; Cognitive behavioral therapy for insomnia; Medications when appropriate; Lifestyle modifications; Treatment of underlying conditions; Sleep study evaluation",
                "when_to_see_doctor": "Chronic insomnia; Loud snoring with breathing pauses; Excessive daytime sleepiness; Unrefreshing sleep despite adequate time; Unusual behaviors during sleep; Sleep problems affecting daily life; Partner reports breathing problems",
                "prevention": "Maintain regular sleep schedule; Create comfortable sleep environment; Limit caffeine and alcohol; Exercise regularly (not close to bedtime); Manage stress; Avoid large meals before bed; Limit screen time before sleep",
                "how_common": "Very common - affects 50-70 million Americans. Sleep apnea affects 22 million Americans. Insomnia affects 30% of adults. Many sleep disorders are underdiagnosed and untreated."
            },
            
            {
                "name": "General Viral Illness",
                "overview": "General viral illness refers to common viral infections that cause non-specific symptoms affecting multiple body systems. These illnesses are typically self-limiting and resolve within days to weeks with supportive care.",
                "symptoms": "Fatigue and malaise; Low-grade fever; Body aches; Headache; Mild respiratory symptoms; Reduced appetite; Generalized weakness; Mild nausea; Lymph node swelling; Skin rash (sometimes)",
                "causes": "Various common viruses; Seasonal viral circulation; Person-to-person transmission; Respiratory droplets; Contact with contaminated surfaces; Weakened immune system; Stress; Poor nutrition or sleep",
                "treatments": "Rest and adequate sleep; Increased fluid intake; Over-the-counter symptom relief; Gradual return to activities; Symptomatic treatment; Avoid unnecessary antibiotics; Supportive care; Monitor for complications",
                "when_to_see_doctor": "High fever or persistent symptoms; Difficulty breathing; Severe headache; Signs of dehydration; Symptoms lasting more than 10 days; Worsening instead of improving; Severe fatigue or weakness",
                "prevention": "Frequent handwashing; Avoid close contact with sick individuals; Cover coughs and sneezes; Disinfect surfaces; Maintain healthy immune system; Get adequate rest; Stay hydrated; Manage stress",
                "how_common": "Very common - most people experience several viral illnesses each year. More frequent during fall and winter months. Usually mild and self-limiting but can vary in severity."
            },
            
            {
                "name": "Stress-Related Symptoms",
                "overview": "Stress-related symptoms occur when the body's response to physical or emotional stress manifests as physical symptoms. These can affect multiple body systems and significantly impact daily functioning and quality of life.",
                "symptoms": "Headaches; Muscle tension and pain; Fatigue; Sleep disturbances; Digestive problems; Anxiety and irritability; Difficulty concentrating; Changes in appetite; Frequent illnesses; Mood changes",
                "causes": "Work stress; Relationship problems; Financial worries; Major life changes; Chronic illness; Academic pressure; Social stress; Poor coping skills; Lack of support; Perfectionism",
                "treatments": "Stress management techniques; Regular exercise; Relaxation training; Counseling or therapy; Lifestyle modifications; Time management; Social support; Mindfulness practices; Adequate sleep; Healthy diet",
                "when_to_see_doctor": "Severe or persistent symptoms; Inability to cope with daily stress; Physical symptoms affecting health; Depression or anxiety; Substance use to cope; Thoughts of self-harm; Need for professional stress management",
                "prevention": "Learn stress management techniques; Maintain work-life balance; Exercise regularly; Get adequate sleep; Build strong support network; Practice relaxation; Manage time effectively; Set realistic goals; Seek help early",
                "how_common": "Very common - stress affects nearly everyone. 77% of people experience physical symptoms of stress. Chronic stress affects 33% of adults. More recognition and treatment needed."
            },
            
            {
                "name": "Minor Acute Illness",
                "overview": "Minor acute illness refers to short-term health conditions that are typically not serious and resolve on their own or with minimal treatment. These illnesses are common and usually don't require extensive medical intervention.",
                "symptoms": "Mild to moderate symptoms; Short duration (days to weeks); Fatigue; Minor aches and pains; Mild fever; Reduced energy; Temporary discomfort; Usually affects one body system primarily",
                "causes": "Viral infections; Minor bacterial infections; Environmental factors; Stress; Poor sleep; Dietary factors; Seasonal changes; Minor injuries; Overexertion; Exposure to irritants",
                "treatments": "Rest and supportive care; Over-the-counter medications; Increased fluid intake; Symptomatic treatment; Time for natural recovery; Avoid overexertion; Monitor symptoms; Return to normal activities gradually",
                "when_to_see_doctor": "Symptoms worsen or persist; High fever; Severe pain; Signs of serious infection; Chronic underlying conditions; Unusual or concerning symptoms; Difficulty functioning; Prevention needs",
                "prevention": "Maintain healthy lifestyle; Regular exercise; Adequate sleep; Stress management; Good hygiene; Balanced nutrition; Avoid known triggers; Stay up-to-date with vaccinations; Regular check-ups",
                "how_common": "Very common - most people experience several minor acute illnesses each year. Usually resolve without complications. Important to distinguish from more serious conditions."
            }
        ]
        
        # Add diseases to database using direct SQL instead of ORM to avoid schema issues
        added_count = 0
        for disease_data in standardized_diseases:
            try:
                # Check if disease already exists using direct SQL
                existing_check = db.execute(text(
                    "SELECT COUNT(*) FROM diseases WHERE name = :name"
                ), {"name": disease_data["name"]}).fetchone()
                
                if existing_check[0] == 0:
                    # Insert new disease using direct SQL
                    insert_sql = text("""
                        INSERT INTO diseases (name, overview, symptoms, causes, treatments, when_to_see_doctor, prevention, how_common)
                        VALUES (:name, :overview, :symptoms, :causes, :treatments, :when_to_see_doctor, :prevention, :how_common)
                    """)
                    
                    db.execute(insert_sql, disease_data)
                    added_count += 1
                    print(f"✅ Added: {disease_data['name']}")
                else:
                    # Update existing disease using direct SQL
                    update_sql = text("""
                        UPDATE diseases SET 
                            overview = :overview,
                            symptoms = :symptoms,
                            causes = :causes,
                            treatments = :treatments,
                            when_to_see_doctor = :when_to_see_doctor,
                            prevention = :prevention,
                            how_common = :how_common
                        WHERE name = :name
                    """)
                    
                    db.execute(update_sql, disease_data)
                    print(f"🔄 Updated: {disease_data['name']}")
                    
            except Exception as disease_error:
                print(f"❌ Error processing {disease_data['name']}: {disease_error}")
                continue
        
        db.commit()
        
        # Show final count using direct SQL
        try:
            total_count = db.execute(text("SELECT COUNT(*) FROM diseases")).fetchone()[0]
            print(f"\n🎯 Disease standardization complete!")
            print(f"📊 Total diseases in database: {total_count}")
            print(f"📝 Added/Updated: {len(standardized_diseases)} standardized diseases")
        except Exception as e:
            print(f"⚠️  Could not get final count: {e}")
        
    except Exception as e:
        print(f"❌ Error adding standardized diseases: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    print("🏥 IPHC Disease Information Standardization")
    print("=" * 50)
    print("This will replace generic disease info with comprehensive medical details")
    print("Including your specific symptoms, causes, treatments, and 'how common' data")
    print("Using direct SQL to avoid schema conflicts")
    print()
    add_standardized_diseases()

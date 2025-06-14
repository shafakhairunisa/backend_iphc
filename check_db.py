from config.database import SessionLocal
from models.disease_model import Disease

db = SessionLocal()
try:
    diseases = db.query(Disease).all()
    print(f'Database has {len(diseases)} diseases')
    
    for d in diseases[:3]:
        print(f'- Name: "{d.name}"')
        print(f'- Overview: {d.overview[:100]}...')
        print('---')
        
    # Test specific disease
    viral_infection = db.query(Disease).filter(Disease.name == 'Viral Infection').first()
    if viral_infection:
        print(f'\nFound "Viral Infection":')
        print(f'Overview: {viral_infection.overview[:150]}...')
    else:
        print('\n"Viral Infection" not found in database!')
        
finally:
    db.close()

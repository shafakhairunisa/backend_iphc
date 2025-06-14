from config.database import SessionLocal, engine
from models.disease_model import Disease
import sys

def populate_diseases():
    """Populate the diseases table with standardized disease information"""
    try:
        # First, create the table if it doesn't exist
        Disease.__table__.create(engine, checkfirst=True)
        
        db = SessionLocal()
        
        # Check if diseases already exist
        existing_count = db.query(Disease).count()
        if existing_count > 0:
            print(f"Found {existing_count} existing diseases. Do you want to clear and repopulate? (y/n)")
            choice = input().lower()
            if choice == 'y':
                db.query(Disease).delete()
                db.commit()
                print("Cleared existing disease data.")
            else:
                print("Keeping existing data. Exiting.")
                return
        
        # Read and execute the SQL file
        with open('populate_diseases.sql', 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Execute the SQL
        db.execute(sql_content)
        db.commit()
        
        # Verify the data was inserted
        disease_count = db.query(Disease).count()
        print(f"Successfully populated {disease_count} diseases in the database!")
        
        # Show a few examples
        sample_diseases = db.query(Disease).limit(3).all()
        print("\nSample diseases added:")
        for disease in sample_diseases:
            print(f"- {disease.name}: {disease.overview[:100]}...")
            
    except Exception as e:
        print(f"Error populating diseases: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    populate_diseases()

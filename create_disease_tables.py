from config.database import engine, Base
from models.disease_model import Disease
from services.disease_service import populate_sample_diseases

def create_disease_tables():
    """Create disease tables and populate with sample data"""
    print("Creating disease tables...")
    Base.metadata.create_all(bind=engine)
    print("Disease tables created successfully!")
    
    print("Populating sample disease data...")
    populate_sample_diseases()
    print("Sample data populated successfully!")

if __name__ == "__main__":
    create_disease_tables()

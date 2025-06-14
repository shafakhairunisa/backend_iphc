from sqlalchemy.orm import Session

def seed_allergies(db: Session):
    """
    Fungsi untuk seed data allergies ke database
    """
    from services import allergy_service
    
    default_allergies = ["Milk", "Shellfish", "Egg", "Wheat", "Peanut", "Fish"]
    
    # Cek apakah data allergies sudah ada
    existing_allergies = allergy_service.get_all_allergies(db)
    if len(existing_allergies) == 0:
        # Tambahkan allergies default jika belum ada data
        for allergy_name in default_allergies:
            if not allergy_service.get_allergy_by_name(db, allergy_name):
                allergy_service.create_allergy(db, {"name": allergy_name})
        print("✅ Default allergies seeded successfully")

def run_seeds():
    """
    Fungsi untuk menjalankan semua seed data
    """
    from config.database import SessionLocal
    
    db = SessionLocal()
    try:
        seed_allergies(db)
    finally:
        db.close()
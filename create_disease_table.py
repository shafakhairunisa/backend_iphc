from config.database import SessionLocal, engine
from models.disease_model import Disease
from sqlalchemy import text

def create_disease_table():
    """Create the diseases table with proper schema"""
    try:
        print("🔧 Creating diseases table...")
        
        # Create all tables from models
        Disease.__table__.create(engine, checkfirst=True)
        
        db = SessionLocal()
        
        # Check if table was created successfully (MySQL version)
        result = db.execute(text("SHOW TABLES LIKE 'diseases'")).fetchone()
        if result:
            print("✅ Diseases table created successfully!")
            
            # Check table structure (MySQL version)
            columns = db.execute(text("DESCRIBE diseases")).fetchall()
            print("\n📋 Table structure:")
            for col in columns:
                print(f"   - {col[0]}: {col[1]} {'NULL' if col[2] == 'YES' else 'NOT NULL'}")
                
        else:
            print("❌ Failed to create diseases table")
            
    except Exception as e:
        print(f"❌ Error creating diseases table: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

def drop_and_recreate_table():
    """Drop existing table and recreate it (use with caution!)"""
    try:
        print("⚠️  WARNING: This will delete all existing disease data!")
        choice = input("Continue? (y/N): ").lower()
        if choice != 'y':
            print("Cancelled.")
            return
            
        db = SessionLocal()
        
        # Drop table if exists (MySQL version)
        db.execute(text("DROP TABLE IF EXISTS diseases"))
        db.commit()
        print("🗑️  Dropped existing diseases table")
        
        # Recreate table
        Disease.__table__.create(engine, checkfirst=False)
        print("✅ Recreated diseases table")
        
    except Exception as e:
        print(f"❌ Error recreating table: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

def check_existing_data():
    """Check if diseases table exists and has data"""
    try:
        db = SessionLocal()
        
        # Check if table exists
        result = db.execute(text("SHOW TABLES LIKE 'diseases'")).fetchone()
        if result:
            print("✅ Diseases table exists")
            
            # Count existing records
            count = db.execute(text("SELECT COUNT(*) FROM diseases")).fetchone()[0]
            print(f"📊 Current records: {count}")
            
            if count > 0:
                # Show sample records
                samples = db.execute(text("SELECT name FROM diseases LIMIT 3")).fetchall()
                print("📋 Sample diseases:")
                for sample in samples:
                    print(f"   - {sample[0]}")
        else:
            print("❌ Diseases table does not exist")
            
    except Exception as e:
        print(f"❌ Error checking table: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Disease Table Management\n")
    print("1. Create diseases table")
    print("2. Check existing data")
    print("3. Drop and recreate table (DANGEROUS)")
    print("4. Exit")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        create_disease_table()
    elif choice == "2":
        check_existing_data()
    elif choice == "3":
        drop_and_recreate_table()
    elif choice == "4":
        print("Goodbye!")
    else:
        print("Invalid option")
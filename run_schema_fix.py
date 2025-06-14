from config.database import SessionLocal, engine
from sqlalchemy import text

def fix_database_schema():
    """Fix database schema to match expected structure"""
    try:
        db = SessionLocal()
        
        # First, let's check current table structure
        print("Checking current table structure...")
        try:
            result = db.execute(text("DESCRIBE diseases")).fetchall()
            print("Current columns:")
            for row in result:
                print(f"  - {row[0]}: {row[1]}")
        except Exception as e:
            print(f"Error checking table structure: {e}")
        
        # Try to add how_common column if it doesn't exist
        try:
            db.execute(text("ALTER TABLE diseases ADD COLUMN how_common TEXT"))
            db.commit()
            print("Added how_common column")
        except Exception as e:
            print(f"Column how_common might already exist: {e}")
        
        # Update some diseases with commonality info
        updates = [
            ("Common Cold", "Very common - affects millions annually, especially during cold and flu seasons"),
            ("Gastroenteritis", "Very common - one of the most frequent digestive complaints, affecting people of all ages"),
            ("Migraine", "Common - affects about 12% of the global population, more frequent in developed countries"),
            ("Tension Headache", "Very common - most people experience tension headaches occasionally, affecting up to 80% of adults"),
            ("Viral Infection", "Common - viral infections are among the most frequent reasons for medical visits"),
            ("Food Poisoning", "Very common - millions of cases occur annually, especially from contaminated food or water")
        ]
        
        for disease_name, commonality in updates:
            try:
                db.execute(text(
                    "UPDATE diseases SET how_common = :commonality WHERE name = :name AND (how_common IS NULL OR how_common = '')"
                ), {"commonality": commonality, "name": disease_name})
                print(f"Updated {disease_name}")
            except Exception as e:
                print(f"Error updating {disease_name}: {e}")
        
        db.commit()
        
        # Verify the updates
        result = db.execute(text("SELECT COUNT(*) FROM diseases WHERE how_common IS NOT NULL AND how_common != ''")).fetchone()
        count = result[0] if result else 0
        print(f"Successfully updated {count} diseases with commonality information!")
        
        # Test a sample query
        test_result = db.execute(text("SELECT name, how_common FROM diseases WHERE name = 'Common Cold'")).fetchone()
        if test_result:
            print(f"Test query result: {test_result[0]} - {test_result[1][:50]}...")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_database_schema()

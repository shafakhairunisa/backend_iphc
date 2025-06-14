from config.database import SessionLocal, engine
from sqlalchemy import text

def execute_sql_file():
    """Execute the populate_diseases.sql file using your existing database setup"""
    try:
        # Create session
        db = SessionLocal()
        
        # Read SQL file
        with open('populate_diseases.sql', 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Split statements and execute
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        for statement in statements:
            if statement:
                print(f"Executing: {statement[:50]}...")
                db.execute(text(statement))
        
        db.commit()
        
        # Verify insertion
        result = db.execute(text("SELECT COUNT(*) FROM diseases")).fetchone()
        count = result[0] if result else 0
        print(f"Successfully inserted/updated diseases! Total count: {count}")
        
        # Show sample
        samples = db.execute(text("SELECT name FROM diseases LIMIT 5")).fetchall()
        print("Sample diseases:")
        for sample in samples:
            print(f"- {sample[0]}")
            
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    execute_sql_file()

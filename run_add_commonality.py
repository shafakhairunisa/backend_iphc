from config.database import SessionLocal, engine
from sqlalchemy import text

def add_commonality_info():
    """Add how_common column and populate with data"""
    try:
        db = SessionLocal()
        
        # Read and execute SQL file
        with open('add_commonality_column.sql', 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Split statements and execute
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        for statement in statements:
            if statement:
                print(f"Executing: {statement[:50]}...")
                db.execute(text(statement))
        
        db.commit()
        
        # Verify updates
        result = db.execute(text("SELECT COUNT(*) FROM diseases WHERE how_common IS NOT NULL")).fetchone()
        count = result[0] if result else 0
        print(f"Successfully updated {count} diseases with commonality information!")
        
        # Show samples
        samples = db.execute(text("SELECT name, how_common FROM diseases WHERE how_common IS NOT NULL LIMIT 3")).fetchall()
        print("\nSample commonality info:")
        for sample in samples:
            print(f"- {sample[0]}: {sample[1][:60]}...")
            
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_commonality_info()

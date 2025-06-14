from sqlalchemy import create_engine, text, pool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import sqlalchemy

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# 1. Deklarasi Base di awal
Base = declarative_base()

# 2. URL DB
TEMP_DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}"
REAL_DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Add connection pooling and reconnection settings
engine = create_engine(
    REAL_DB_URL,
    poolclass=pool.QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Validates connections before use
    pool_recycle=3600,   # Recycle connections every hour
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def ensure_database():
    try:
        test_engine = create_engine(REAL_DB_URL)
        conn = test_engine.connect()
        conn.close()
    except sqlalchemy.exc.OperationalError:
        print(f"\n⚠️  Database '{DB_NAME}' belum tersedia.")
        pilihan = input("❓ Ingin membuat database tersebut sekarang? (y/n): ").strip().lower()
        if pilihan == "y":
            tmp_engine = create_engine(TEMP_DB_URL)
            tmp_conn = tmp_engine.connect()
            tmp_conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`"))
            tmp_conn.close()
            print(f"✅ Database '{DB_NAME}' berhasil dibuat.")
        else:
            print("❌ Database tidak dibuat. Program dihentikan.")
            exit()

# 3. Jalankan pengecekan dan inisialisasi koneksi
ensure_database()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Inisialisasi database dan buat semua tabel"""
    # Import all models to ensure they're registered with Base
    from models import user_model, prediction_model, allergy_model
    
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")
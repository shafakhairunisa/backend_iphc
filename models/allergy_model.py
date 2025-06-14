from sqlalchemy import Column, Integer, String
from config.database import Base

class Allergy(Base):
    __tablename__ = "allergies"
    
    allergy_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
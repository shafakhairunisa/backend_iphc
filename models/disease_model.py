from sqlalchemy import Column, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Disease(Base):
    __tablename__ = "diseases"
    
    # FIXED: Use name as primary key instead of id
    name = Column(String(255), primary_key=True)
    overview = Column(Text)
    symptoms = Column(Text) 
    causes = Column(Text)
    treatments = Column(Text)
    when_to_see_doctor = Column(Text)
    prevention = Column(Text)
    how_common = Column(Text)
    
    def __repr__(self):
        return f"<Disease(name='{self.name}')>"

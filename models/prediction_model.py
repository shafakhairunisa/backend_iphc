from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base

class Prediction(Base):
    __tablename__ = "predictions"
    
    predict_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    main_symptom = Column(String(255))
    other_symptoms = Column(Text)
    duration = Column(String(50))
    severity = Column(String(50))
    top_results = Column(JSON)
    dynamic_answers = Column(JSON, nullable=True)
    user_journey = Column(JSON, nullable=True)
    assessment_summary = Column(Text, nullable=True)
    total_symptoms_count = Column(Integer, nullable=True)
    assessment_timestamp = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="predictions")
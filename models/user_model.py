from sqlalchemy import Column, Integer, String, Text
from config.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255))
    username = Column(String(255), unique=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))
    birthday = Column(String(20))
    gender = Column(String(10))
    height = Column(String(10))
    weight = Column(String(10))
    blood_type = Column(String(5))
    allergies = Column(Text)

    predictions = relationship("Prediction", back_populates="user")
    documents = relationship("Document", back_populates="user")

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"
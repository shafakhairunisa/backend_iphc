from sqlalchemy.orm import Session
from models.allergy_model import Allergy
from typing import List, Optional

def get_all_allergies(db: Session) -> List[Allergy]:
    return db.query(Allergy).all()

def get_allergy_by_id(db: Session, allergy_id: int) -> Optional[Allergy]:
    return db.query(Allergy).filter(Allergy.allergy_id == allergy_id).first()

def get_allergy_by_name(db: Session, name: str) -> Optional[Allergy]:
    return db.query(Allergy).filter(Allergy.name == name).first()

def create_allergy(db: Session, data: dict) -> Allergy:
    allergy = Allergy(name=data["name"])
    db.add(allergy)
    db.commit()
    db.refresh(allergy)
    return allergy

def update_allergy(db: Session, allergy_id: int, data: dict) -> Optional[Allergy]:
    allergy = get_allergy_by_id(db, allergy_id)
    if allergy:
        allergy.name = data["name"]
        db.commit()
        db.refresh(allergy)
    return allergy

def delete_allergy(db: Session, allergy_id: int) -> Optional[Allergy]:
    allergy = get_allergy_by_id(db, allergy_id)
    if allergy:
        db.delete(allergy)
        db.commit()
    return allergy
from fastapi import HTTPException, Request, Depends
from sqlalchemy.orm import Session
import services.allergy_service as allergy_service
from config.database import get_db

def get_allergies(request: Request, db: Session):
    result = allergy_service.get_all_allergies(db)
    allergies = []
    for allergy in result:
        allergies.append({
            "id": allergy.allergy_id,  # Frontend expects 'id', not 'allergy_id'
            "name": allergy.name
        })
    
    # Return format that matches what frontend expects
    return allergies

def get_allergy(allergy_id: int, request: Request, db: Session):
    allergy = allergy_service.get_allergy_by_id(db, allergy_id)
    if not allergy:
        raise HTTPException(status_code=404, detail="Allergy not found")
    return {
        "success": True,
        "message": f"Allergy with ID {allergy_id} retrieved successfully",
        "data": {
            "allergy_id": allergy.allergy_id,
            "name": allergy.name
        }
    }

def create_allergy(data: dict, request: Request, db: Session):
    try:
        result = allergy_service.create_allergy(db, data)
        return {
            "success": True,
            "message": "Allergy created successfully",
            "data": {
                "allergy_id": result.allergy_id,
                "name": result.name
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def update_allergy(allergy_id: int, data: dict, request: Request, db: Session):
    try:
        result = allergy_service.update_allergy(db, allergy_id, data)
        if not result:
            raise HTTPException(status_code=404, detail="Allergy not found")
        return {
            "success": True,
            "message": "Allergy updated successfully",
            "data": {
                "allergy_id": result.allergy_id,
                "name": result.name
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def delete_allergy(allergy_id: int, db: Session):
    allergy = allergy_service.delete_allergy(db, allergy_id)
    if not allergy:
        raise HTTPException(status_code=404, detail="Allergy not found")
    return {"success": True, "message": f"Allergy with ID {allergy_id} deleted successfully", "data": None}
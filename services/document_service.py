from sqlalchemy.orm import Session
from models.document_model import Document
from config.database import SessionLocal
from typing import List, Optional
import os
import base64
from datetime import datetime

def save_document(user_id: int, filename: str, file_content: str, file_type: str) -> dict:
    """Save document to database with extracted content"""
    try:
        db = SessionLocal()
        
        # Calculate file size (rough estimate from base64 if applicable)
        file_size = len(file_content.encode('utf-8'))
        
        # Create document record
        document = Document(
            user_id=user_id,
            filename=filename,
            file_type=file_type.lower(),
            file_size=file_size,
            extracted_text=file_content,
            upload_date=datetime.now()
        )
        
        db.add(document)
        db.commit()
        db.refresh(document)
        
        return {
            "success": True,
            "document_id": document.document_id,
            "message": "Document saved successfully"
        }
        
    except Exception as e:
        print(f"DEBUG: Error saving document: {e}")
        if 'db' in locals():
            db.rollback()
        return {
            "success": False,
            "message": f"Failed to save document: {str(e)}"
        }
    finally:
        if 'db' in locals():
            db.close()

def get_user_documents(user_id: int) -> List[dict]:
    """Get all documents for a user"""
    try:
        db = SessionLocal()
        documents = db.query(Document).filter(Document.user_id == user_id).order_by(Document.upload_date.desc()).all()
        
        result = []
        for doc in documents:
            result.append({
                "document_id": doc.document_id,
                "filename": doc.filename,
                "file_type": doc.file_type,
                "file_size": doc.file_size,
                "extracted_text": doc.extracted_text,
                "upload_date": doc.upload_date.isoformat() if doc.upload_date else None
            })
        
        return result
        
    except Exception as e:
        print(f"DEBUG: Error getting documents: {e}")
        return []
    finally:
        if 'db' in locals():
            db.close()

def get_document_by_id(document_id: int) -> Optional[dict]:
    """Get a specific document by ID"""
    try:
        db = SessionLocal()
        document = db.query(Document).filter(Document.document_id == document_id).first()
        
        if document:
            return {
                "document_id": document.document_id,
                "user_id": document.user_id,
                "filename": document.filename,
                "file_type": document.file_type,
                "file_size": document.file_size,
                "extracted_text": document.extracted_text,
                "upload_date": document.upload_date.isoformat() if document.upload_date else None
            }
        
        return None
        
    except Exception as e:
        print(f"DEBUG: Error getting document: {e}")
        return None
    finally:
        if 'db' in locals():
            db.close()

def delete_document(document_id: int, user_id: int) -> dict:
    """Delete a document"""
    try:
        db = SessionLocal()
        document = db.query(Document).filter(
            Document.document_id == document_id,
            Document.user_id == user_id
        ).first()
        
        if document:
            db.delete(document)
            db.commit()
            return {
                "success": True,
                "message": "Document deleted successfully"
            }
        else:
            return {
                "success": False,
                "message": "Document not found"
            }
            
    except Exception as e:
        print(f"DEBUG: Error deleting document: {e}")
        if 'db' in locals():
            db.rollback()
        return {
            "success": False,
            "message": f"Failed to delete document: {str(e)}"
        }
    finally:
        if 'db' in locals():
            db.close()

from fastapi import APIRouter, HTTPException, Body
from services.document_service import save_document, get_user_documents, get_document_by_id, delete_document

router = APIRouter()

@router.post("/upload")
async def upload_document(request: dict = Body(...)):
    """Upload and save a document"""
    try:
        user_id = request.get('user_id')
        filename = request.get('filename')
        file_content = request.get('file_content')
        file_type = request.get('file_type')
        
        if not all([user_id, filename, file_content, file_type]):
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        result = save_document(user_id, filename, file_content, file_type)
        
        if result['success']:
            return result
        else:
            raise HTTPException(status_code=500, detail=result['message'])
            
    except Exception as e:
        print(f"DEBUG: Error in upload_document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}")
async def get_user_documents_endpoint(user_id: int):
    """Get all documents for a user"""
    try:
        documents = get_user_documents(user_id)
        return documents
    except Exception as e:
        print(f"DEBUG: Error getting user documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{document_id}")
async def get_document_endpoint(document_id: int):
    """Get a specific document"""
    try:
        document = get_document_by_id(document_id)
        if document:
            return document
        else:
            raise HTTPException(status_code=404, detail="Document not found")
    except Exception as e:
        print(f"DEBUG: Error getting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{document_id}")
async def delete_document_endpoint(document_id: int, request: dict = Body(...)):
    """Delete a document"""
    try:
        user_id = request.get('user_id')
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID required")
        
        result = delete_document(document_id, user_id)
        
        if result['success']:
            return result
        else:
            raise HTTPException(status_code=404, detail=result['message'])
            
    except Exception as e:
        print(f"DEBUG: Error deleting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

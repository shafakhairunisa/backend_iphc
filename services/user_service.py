import os
import base64
from datetime import datetime
from models.user_model import User
from config.database import SessionLocal
from utils.email_utils import send_otp_email, verify_otp, generate_otp

UPLOAD_DIR = "assets/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_photo(photo_b64: str, user_id: int) -> str:
    if not photo_b64:
        return None
    try:
        img_data = base64.b64decode(photo_b64)
    except Exception:
        raise ValueError("Invalid image format")
    filename = f"user_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(img_data)
    return filepath

def get_all_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users

def create_user(data: dict):
    db = SessionLocal()
    try:
        photo_b64 = data.pop("photo", None)
        new_user = User(**data)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        if photo_b64:
            new_user.photo = save_photo(photo_b64, new_user.user_id)
            db.commit()
            db.refresh(new_user)
        return new_user
    finally:
        db.close()

def update_user(user_id: int, data: dict):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            photo_b64 = data.pop("photo", None)
            if photo_b64:
                if user.photo and os.path.exists(user.photo):
                    os.remove(user.photo)
                user.photo = save_photo(photo_b64, user_id)
            for key, value in data.items():
                setattr(user, key, value)
            db.commit()
            db.refresh(user)
        return user
    finally:
        db.close()

def delete_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    db.close()
    return user

def find_user_by_email(email: str):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    db.close()
    return user

def authenticate_user(email, password):
    db = SessionLocal()
    try:
        # Add retry logic for database connections
        user = db.query(User).filter(User.email == email, User.password == password).first()
        return user
    except Exception as e:
        print(f"Database error in authenticate_user: {e}")
        db.rollback()
        # Try once more with a fresh connection
        try:
            db.close()
            db = SessionLocal()
            user = db.query(User).filter(User.email == email, User.password == password).first()
            return user
        except Exception as retry_error:
            print(f"Retry failed: {retry_error}")
            return None
    finally:
        db.close()

def request_password_reset(email: str) -> bool:
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return False
        
        otp = generate_otp()
        success = send_otp_email(email, otp)
        return success
    finally:
        db.close()

def verify_password_reset_otp(email: str, otp_code: str) -> dict:
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return {"success": False, "message": "Email not found"}
        
        if verify_otp(email, otp_code):
            return {
                "success": True, 
                "message": "OTP verified successfully",
                "user_id": user.user_id
            }
        else:
            return {"success": False, "message": "Invalid or expired OTP"}
    finally:
        db.close()

def reset_password(email: str, new_password: str) -> dict:
    """Reset password menggunakan email (setelah verifikasi OTP)"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return {"success": False, "message": "Email not found"}
        
        user.password = new_password
        db.commit()
        db.refresh(user)
        
        return {
            "success": True,
            "message": "Password updated successfully",
            "user_id": user.user_id
        }
    except Exception as e:
        db.rollback()
        return {"success": False, "message": f"Error updating password: {str(e)}"}
    finally:
        db.close()

async def update_user_service(user_id: int, data: dict):
    """Update user service with comprehensive validation"""
    db = SessionLocal()
    try:
        print(f"DEBUG: Service updating user {user_id}")
        print(f"DEBUG: Received data: {data}")
        
        # Check if user exists
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            return {"success": False, "message": "User not found"}
        
        # Update allowed fields (ONLY fields that exist in your database)
        allowed_fields = [
            'name', 'email', 'birthday', 'gender', 
            'height', 'weight', 'blood_type', 'allergies'
        ]
        
        updated_fields = []
        for field in allowed_fields:
            if field in data:
                old_value = getattr(user, field, None)
                new_value = data[field]
                
                # Special handling for birthday field
                if field == 'birthday':
                    print(f"DEBUG: Processing birthday field: '{new_value}'")
                    if new_value and new_value not in ['', '0000-00-00', None]:
                        # Keep the birthday as-is from frontend
                        setattr(user, field, str(new_value))
                        updated_fields.append(field)
                        print(f"DEBUG: Updated birthday: {old_value} -> {new_value}")
                    else:
                        print(f"DEBUG: Skipping invalid birthday: '{new_value}'")
                else:
                    # Regular field update
                    if new_value is not None:
                        setattr(user, field, str(new_value))
                        updated_fields.append(field)
                        print(f"DEBUG: Updated {field}: {old_value} -> {new_value}")
        
        if not updated_fields:
            return {"success": False, "message": "No valid fields to update"}
        
        # Commit changes
        db.commit()
        db.refresh(user)
        
        print(f"DEBUG: Successfully updated fields: {updated_fields}")
        print(f"DEBUG: User birthday after update: '{user.birthday}'")
        
        # Return updated user data (ONLY fields that exist)
        user_data = {
            "user_id": user.user_id,
            "name": getattr(user, 'name', ''),
            "username": getattr(user, 'username', ''),
            "email": getattr(user, 'email', ''),
            "birthday": getattr(user, 'birthday', ''),
            "gender": getattr(user, 'gender', ''),
            "height": getattr(user, 'height', ''),
            "weight": getattr(user, 'weight', ''),
            "blood_type": getattr(user, 'blood_type', ''),
            "allergies": getattr(user, 'allergies', '')
        }
        
        print(f"DEBUG: Returning user data with birthday: '{user_data['birthday']}'")
        
        return {
            "success": True,
            "message": f"Updated {len(updated_fields)} fields successfully",
            "user": user_data,
            "updated_fields": updated_fields
        }
        
    except Exception as e:
        print(f"DEBUG: Database error in update_user_service: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
        return {"success": False, "message": f"Database error: {str(e)}"}
    finally:
        db.close()

def get_user_by_id(user_id: int):
    """Get user by ID with safe field access"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            return None
        
        # Return user object with safe attribute access
        return user
    except Exception as e:
        print(f"DEBUG: Database error in get_user_by_id: {e}")
        return None
    finally:
        db.close()

class UserService:
    """Service class for user operations - wrapper around existing functions"""
    
    @staticmethod
    def authenticate_user(email: str, password: str):
        """Authenticate user wrapper"""
        return authenticate_user(email, password)
    
    @staticmethod
    def create_user(data: dict):
        """Create user wrapper"""
        return create_user(data)
    
    @staticmethod
    def update_user(user_id: int, data: dict):
        """Update user wrapper"""
        return update_user(user_id, data)
    
    @staticmethod
    def delete_user(user_id: int):
        """Delete user wrapper"""
        return delete_user(user_id)
    
    @staticmethod
    def get_user_by_id(user_id: int):
        """Get user by ID wrapper"""
        return get_user_by_id(user_id)
    
    @staticmethod
    def find_user_by_email(email: str):
        """Find user by email wrapper"""
        return find_user_by_email(email)
    
    @staticmethod
    def request_password_reset(email: str):
        """Request password reset wrapper"""
        return request_password_reset(email)
    
    @staticmethod
    def verify_password_reset_otp(email: str, otp_code: str):
        """Verify password reset OTP wrapper"""
        return verify_password_reset_otp(email, otp_code)
    
    @staticmethod
    def reset_password(email: str, new_password: str):
        """Reset password wrapper"""
        return reset_password(email, new_password)
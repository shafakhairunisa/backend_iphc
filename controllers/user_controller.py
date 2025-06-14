from fastapi import HTTPException
from services.user_service import *
from datetime import datetime

def format_date(date_obj):
    """Handle both string and datetime objects"""
    if date_obj is None:
        return None
    
    # If it's already a string, return as is
    if isinstance(date_obj, str):
        return date_obj
    
    # If it's a datetime object, format it
    if hasattr(date_obj, 'strftime'):
        return date_obj.strftime("%d/%m/%Y")
    
    # Fallback - convert to string
    return str(date_obj)

async def update_user_controller(user_id: int, data: dict):
    """Update user with better error handling and validation"""
    try:
        print(f"DEBUG: Updating user {user_id} with data: {list(data.keys())}")
        
        # Validate required fields
        if not data:
            return {"success": False, "message": "No data provided"}
        
        # Handle profile_photo vs photo field mapping
        if 'photo' in data and 'profile_photo' not in data:
            data['profile_photo'] = data.pop('photo')
        
        # Call service layer
        result = await update_user_service(user_id, data)
        
        if result.get("success"):
            print(f"DEBUG: User {user_id} updated successfully")
            return {
                "success": True,
                "message": "Profile updated successfully",
                "user": result.get("user", {})
            }
        else:
            print(f"DEBUG: User update failed: {result.get('message')}")
            return {
                "success": False,
                "message": result.get("message", "Update failed")
            }
            
    except Exception as e:
        print(f"DEBUG: Error in update_user_controller: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "message": f"Controller error: {str(e)}"}

async def get_user_controller(user_id: int):
    try:
        result = get_user_by_id(user_id)
        
        if result:
            # FIXED: Ensure all values are never None
            user_data = {
                "user_id": result.user_id or 0,
                "name": getattr(result, 'name', '') or '',
                "username": getattr(result, 'username', '') or '',
                "email": getattr(result, 'email', '') or '',
                "birthday": format_date(getattr(result, 'birthday', '')) or '',
                "gender": getattr(result, 'gender', '') or '',
                "height": getattr(result, 'height', '') or '',
                "weight": getattr(result, 'weight', '') or '',
                "blood_type": getattr(result, 'blood_type', '') or '',
                "allergies": getattr(result, 'allergies', '') or ''
            }
            return {"success": True, "user": user_data}
        else:
            return {"success": False, "message": "User not found"}
    except Exception as e:
        print(f"DEBUG: Error in get_user_controller: {e}")
        return {"success": False, "message": str(e)}

def authenticate_user(email: str, password: str):
    """Authenticate user with email and password"""
    try:
        print(f"DEBUG: Authenticating user with email: {email}")
        
        # Call the service layer
        user = find_user_by_email(email)
        
        if not user:
            print(f"DEBUG: No user found with email: {email}")
            return None
        
        print(f"DEBUG: Found user: {user.name}, checking password...")
        
        # Check password (assuming plain text for now - should be hashed in production)
        if user.password == password:
            print(f"DEBUG: Password match for user: {user.name}")
            return user
        else:
            print(f"DEBUG: Password mismatch for user: {user.name}")
            return None
            
    except Exception as e:
        print(f"DEBUG: Error in authenticate_user: {e}")
        import traceback
        traceback.print_exc()
        return None

def get_users(request):
    """Get all users"""
    try:
        users = get_all_users()
        users_data = []
        for user in users:
            user_data = {
                "user_id": user.user_id,
                "name": getattr(user, 'name', ''),
                "email": getattr(user, 'email', ''),
                "username": getattr(user, 'username', ''),
                "gender": getattr(user, 'gender', ''),
                "birthday": format_date(getattr(user, 'birthday', '')),
                "height": getattr(user, 'height', ''),
                "weight": getattr(user, 'weight', ''),
                "blood_type": getattr(user, 'blood_type', ''),
                "allergies": getattr(user, 'allergies', '')
            }
            users_data.append(user_data)
        
        return {"success": True, "users": users_data}
    except Exception as e:
        print(f"DEBUG: Error getting users: {e}")
        return {"success": False, "message": str(e)}

def get_user(user_id: int, request):
    """Get single user by ID"""
    try:
        user = get_user_by_id(user_id)
        
        if not user:
            return {"success": False, "message": "User not found"}
        
        user_data = {
            "user_id": user.user_id,
            "name": getattr(user, 'name', ''),
            "username": getattr(user, 'username', ''),
            "email": getattr(user, 'email', ''),
            "birthday": format_date(getattr(user, 'birthday', '')),
            "gender": getattr(user, 'gender', ''),
            "height": getattr(user, 'height', ''),
            "weight": getattr(user, 'weight', ''),
            "blood_type": getattr(user, 'blood_type', ''),
            "allergies": getattr(user, 'allergies', '')
        }
        
        return {"success": True, "user": user_data}
    except Exception as e:
        print(f"DEBUG: Error getting user: {e}")
        return {"success": False, "message": str(e)}

def register_user(user_data: dict, request=None):
    """Register new user"""
    try:
        print(f"DEBUG: Registering user with email: {user_data.get('email')}")
        
        # Check if user already exists
        existing_user = find_user_by_email(user_data.get('email'))
        if existing_user:
            return {"success": False, "message": "Email already registered"}
        
        # Create new user directly using service function
        from services.user_service import create_user as create_user_service
        new_user = create_user_service(user_data)
        
        print(f"DEBUG: Created user result: {new_user}")
        print(f"DEBUG: Created user type: {type(new_user)}")
        
        if new_user:
            # Handle both dict and object responses
            if isinstance(new_user, dict):
                # If service returns dict, use it directly
                user_data_response = {
                    "user_id": new_user.get('user_id', 0),
                    "name": new_user.get('name', ''),
                    "username": new_user.get('username', ''),
                    "email": new_user.get('email', ''),
                    "birthday": new_user.get('birthday', ''),
                    "gender": new_user.get('gender', ''),
                    "height": new_user.get('height', ''),
                    "weight": new_user.get('weight', ''),
                    "blood_type": new_user.get('blood_type', ''),
                    "allergies": new_user.get('allergies', '')
                }
            else:
                # If service returns object, extract attributes
                user_data_response = {
                    "user_id": getattr(new_user, 'user_id', 0),
                    "name": getattr(new_user, 'name', ''),
                    "username": getattr(new_user, 'username', ''),
                    "email": getattr(new_user, 'email', ''),
                    "birthday": format_date(getattr(new_user, 'birthday', '')),
                    "gender": getattr(new_user, 'gender', ''),
                    "height": getattr(new_user, 'height', ''),
                    "weight": getattr(new_user, 'weight', ''),
                    "blood_type": getattr(new_user, 'blood_type', ''),
                    "allergies": getattr(new_user, 'allergies', '')
                }
            
            return {
                "success": True,
                "message": "User registered successfully",
                "user": user_data_response
            }
        else:
            return {"success": False, "message": "Failed to create user"}
            
    except Exception as e:
        print(f"DEBUG: Error in register_user: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "message": str(e)}

# Alias for backward compatibility
register = register_user

def create_user_controller(user_data: dict, request=None):
    """Create user controller - calls register_user but avoid recursion"""
    return register_user(user_data, request)

# Fix the circular reference issue
def create_user(user_data: dict, request=None):
    """Create user controller - directly call service to avoid recursion"""
    from services.user_service import create_user as create_user_service
    return create_user_service(user_data)

def delete_user(user_id: int):
    """Delete user"""
    try:
        result = delete_user(user_id)
        if result:
            return {"success": True, "message": "User deleted successfully"}
        else:
            return {"success": False, "message": "User not found"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def request_password_reset_controller(request_data: dict):
    """Request password reset OTP"""
    try:
        from services.user_service import send_password_reset_otp
        email = request_data.get('email')
        if not email:
            return {"success": False, "message": "Email is required"}
        
        success = send_password_reset_otp(email)
        if success:
            return {"success": True, "message": "OTP sent to your email"}
        else:
            return {"success": False, "message": "Email not found"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def verify_password_reset_otp_controller(request_data: dict):
    """Verify password reset OTP"""
    try:
        email = request_data.get('email')
        otp_code = request_data.get('otp_code')
        
        if not email or not otp_code:
            return {"success": False, "message": "Email and OTP code are required"}
        
        from services.user_service import verify_otp_code as verify_otp_code_service
        result = verify_otp_code_service(email, otp_code)
        return result
    except Exception as e:
        return {"success": False, "message": str(e)}

def reset_password_controller(request_data: dict):
    """Reset password"""
    try:
        email = request_data.get('email')
        new_password = request_data.get('new_password')
        
        if not email or not new_password:
            return {"success": False, "message": "Email and new password are required"}
        
        from services.user_service import update_user_password as update_user_password_service
        result = update_user_password_service(email, new_password)
        return result
    except Exception as e:
        return {"success": False, "message": str(e)}

class UserController:
    def __init__(self):
        pass

    def register(self, user_data: dict, request=None):
        """Register new user (controller method for route)"""
        return register_user(user_data, request)

    def login(self, user_data: dict, request=None):
        """Login user with email and password"""
        try:
            email = user_data.get('email')
            password = user_data.get('password')
            
            if not email or not password:
                return {"success": False, "message": "Email and password are required"}
            
            print(f"DEBUG: Login attempt for email: {email}")
            
            # Use the existing authenticate_user function
            user = authenticate_user(email, password)
            
            if user:
                print(f"DEBUG: Login successful for user: {email}")
                user_data_response = {
                    "user_id": getattr(user, 'user_id', 0),
                    "name": getattr(user, 'name', ''),
                    "username": getattr(user, 'username', ''),
                    "email": getattr(user, 'email', ''),
                    "birthday": format_date(getattr(user, 'birthday', '')),
                    "gender": getattr(user, 'gender', ''),
                    "height": getattr(user, 'height', ''),
                    "weight": getattr(user, 'weight', ''),
                    "blood_type": getattr(user, 'blood_type', ''),
                    "allergies": getattr(user, 'allergies', '')
                }
                return {
                    "success": True,
                    "message": "Login successful",
                    "user": user_data_response
                }
            else:
                print(f"DEBUG: Login failed for user: {email}")
                return {
                    "success": False,
                    "message": "Invalid email or password"
                }
                
        except Exception as e:
            print(f"DEBUG: Login error: {e}")
            import traceback
            traceback.print_exc()
            return {"success": False, "message": f"Login failed: {str(e)}"}

    def request_password_reset(self, request_data: dict):
        """Request password reset OTP"""
        try:
            email = request_data.get('email')
            if not email:
                return {"success": False, "message": "Email is required"}
            
            print(f"DEBUG: Requesting password reset for email: {email}")
            
            # Check if user exists first
            user = find_user_by_email(email)
            if not user:
                return {"success": False, "message": "Email not found"}
            
            # Send OTP
            from services.user_service import request_password_reset
            success = request_password_reset(email)
            
            if success:
                return {"success": True, "message": "OTP sent to your email"}
            else:
                return {"success": False, "message": "Failed to send OTP"}
                
        except Exception as e:
            print(f"DEBUG: Error in request_password_reset: {e}")
            return {"success": False, "message": f"Error sending OTP: {str(e)}"}

    def verify_password_reset_otp(self, request_data: dict):
        """Verify password reset OTP"""
        try:
            email = request_data.get('email')
            otp_code = request_data.get('otp_code')
            
            if not email or not otp_code:
                return {"success": False, "message": "Email and OTP code are required"}
            
            print(f"DEBUG: Verifying OTP for email: {email}, code: {otp_code}")
            
            from services.user_service import verify_password_reset_otp
            result = verify_password_reset_otp(email, otp_code)
            return result
            
        except Exception as e:
            print(f"DEBUG: Error in verify_password_reset_otp: {e}")
            return {"success": False, "message": f"Error verifying OTP: {str(e)}"}

    def reset_password(self, request_data: dict):
        """Reset password"""
        try:
            email = request_data.get('email')
            new_password = request_data.get('new_password')
            
            if not email or not new_password:
                return {"success": False, "message": "Email and new password are required"}
            
            print(f"DEBUG: Resetting password for email: {email}")
            
            from services.user_service import reset_password
            result = reset_password(email, new_password)
            return result
            
        except Exception as e:
            print(f"DEBUG: Error in reset_password: {e}")
            return {"success": False, "message": f"Error resetting password: {str(e)}"}

    def get_users(self, request):
        """Get all users"""
        return get_users(request)

    def get_user(self, user_id: int, request):
        """Get single user by ID"""
        return get_user(user_id, request)

    def create_user(self, user_data: dict, request=None):
        """Create user controller"""
        return create_user_controller(user_data, request)

    def update_user(self, user_id, data):
        """Update user information"""
        try:
            print(f"DEBUG: Updating user {user_id} with data: {data}")
            from services.user_service import update_user as update_user_service
            result = update_user_service(user_id, data)
            
            if result:
                # Convert result to dict if it's an object
                if hasattr(result, '__dict__'):
                    user_dict = {
                        "user_id": getattr(result, 'user_id', 0),
                        "name": getattr(result, 'name', ''),
                        "username": getattr(result, 'username', ''),
                        "email": getattr(result, 'email', ''),
                        "birthday": format_date(getattr(result, 'birthday', '')),
                        "gender": getattr(result, 'gender', ''),
                        "height": getattr(result, 'height', ''),
                        "weight": getattr(result, 'weight', ''),
                        "blood_type": getattr(result, 'blood_type', ''),
                        "allergies": getattr(result, 'allergies', '')
                    }
                else:
                    user_dict = result
                
                return {"success": True, "message": "User updated successfully", "user": user_dict}
            else:
                return {"success": False, "message": "User not found"}
        except Exception as e:
            print(f"DEBUG: Error updating user: {e}")
            return {"success": False, "message": f"Error updating user: {str(e)}"}

    def delete_user(self, user_id: int):
        """Delete user"""
        try:
            from services.user_service import delete_user as delete_user_service
            result = delete_user_service(user_id)
            if result:
                return {"success": True, "message": "User deleted successfully"}
            else:
                return {"success": False, "message": "User not found"}
        except Exception as e:
            return {"success": False, "message": f"Error deleting user: {str(e)}"}
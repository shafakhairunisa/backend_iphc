from fastapi import APIRouter, HTTPException, Request, Body
from controllers.user_controller import UserController

router = APIRouter()
user_router = router
controller = UserController()

@router.get("/test")
def test_endpoint():
    return {
        "message": "User route is working!",
        "status": "OK",
        "available_endpoints": [
            "/users/login",
            "/users/register", 
            "/users/forgot-password",
            "/users/verify-otp",
            "/users/reset-password",
            "/users/{user_id}",
            "/users/test"
        ]
    }

@router.post("/login")
def login_user(user: dict, request: Request):
    try:
        return controller.login(user, request)
    except Exception as e:
        print(f"DEBUG: Login error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/register")  
def register_user(user: dict = Body(...), request: Request = None):
    return controller.register(user, request)

@router.post("/forgot-password")
def forgot_password(request_data: dict = Body(...)):
    """Request password reset OTP"""
    try:
        return controller.request_password_reset(request_data)
    except Exception as e:
        print(f"DEBUG: Forgot password error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/verify-otp")
def verify_password_otp(request_data: dict = Body(...)):
    """Verify OTP code"""
    try:
        return controller.verify_password_reset_otp(request_data)
    except Exception as e:
        print(f"DEBUG: Verify OTP error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset-password")
def reset_password(request_data: dict = Body(...)):
    """Reset password with OTP verification"""
    try:
        return controller.reset_password(request_data)
    except Exception as e:
        print(f"DEBUG: Reset password error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# General CRUD endpoints (parameter routes - put LAST)
@router.get("/")
def get_users(request: Request):
    return controller.get_users(request)

@router.post("/")
def create_user(user: dict = Body(...), request: Request = None):
    return controller.create_user(user, request)

@router.put("/{user_id}")
async def update_user(user_id: int, request: Request):
    """Update user profile - simplified for existing database schema"""
    try:
        # Parse JSON data
        data = await request.json()
        print(f"DEBUG: Updating user {user_id} with data: {list(data.keys())}")
        
        # Remove any fields that don't exist in database
        if 'photo' in data:
            data.pop('photo')  # Remove photo field since it's not supported
            print("DEBUG: Removed 'photo' field - not supported in current database schema")
        
        if 'profile_photo' in data:
            data.pop('profile_photo')  # Remove profile_photo field
            print("DEBUG: Removed 'profile_photo' field - not supported in current database schema")
        
        # Call the controller
        result = controller.update_user(user_id, data)
        print(f"DEBUG: Controller result: {result}")
        return result
        
    except Exception as e:
        print(f"DEBUG: Exception in update_user route: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "message": f"Server error: {str(e)}"}

@router.delete("/{user_id}")
def delete_user(user_id: int):
    return controller.delete_user(user_id)

@router.get("/{user_id}")  # This MUST be last to avoid catching other routes
def get_user(user_id: int, request: Request):
    return controller.get_user(user_id, request)
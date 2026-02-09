from fastapi import HTTPException  # type: ignore[reportMissingImports]

async def exception_helper(user, functionType: str, existing_user = None):
    if functionType == "create":
        if "@" not in user.email or "." not in user.email:
            raise HTTPException(status_code=400, detail="Invalid email format")
        
        # Fixed: existing_user is a User object or None, not a dict
        if existing_user:
            raise HTTPException(status_code=400, detail="Email is already linked to another account")
        
        if len(user.password) < 8:
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
        if not any(char.isdigit() for char in user.password):
            raise HTTPException(status_code=400, detail="Password must contain at least one number")
        if not any(char.isalpha() for char in user.password):
            raise HTTPException(status_code=400, detail="Password must contain at least one letter")
    
    elif functionType == "get_id":
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
    
    else:
        raise HTTPException(status_code=500, detail="Invalid function type for exception_helper")
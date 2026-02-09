from fastapi import HTTPException, APIRouter # type: ignore[reportMissingImports]
from pydantic import BaseModel # pyright: ignore[reportMissingImports]
from .helper import exception_helper  # pyright: ignore[reportMissingImports]

router = APIRouter()

users: dict[int, dict] = {}
current_id = 1

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

@router.post("/create")
async def create_user(user: UserCreate):
    global current_id
    await exception_helper(user, "create", users)
    # Use model_dump() instead of dict() for Pydantic v2
    users[current_id] = user.model_dump()
    response = {"id": current_id, **user.model_dump()}
    current_id += 1
    return response

@router.get("/list")
async def get_users():
    return [
        {"id": user_id, **user}
        for user_id, user in users.items()
    ]

@router.get("/list/{user_id}")
async def get_user(user_id: int):
    user = users.get(user_id)
    await exception_helper(user, "get_id")
    return {"id": user_id, **user}

@router.put("/update/{user_id}")
async def update_user(user_id: int, user: UserCreate):
    current_user = users.get(user_id)
    await exception_helper(current_user, "get_id")
    users[user_id] = user.model_dump()
    return {"id": user_id, **user.model_dump()}

@router.delete("/delete/{user_id}")
async def delete_user(user_id: int):
    current_user = users.get(user_id)
    await exception_helper(current_user, "get_id")
    del users[user_id]
    return {"detail": "User deleted successfully"}
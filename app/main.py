from fastapi import FastAPI # type: ignore[reportMissingImports]
from .users import router as users_router
from .database import init_db

app = FastAPI(
    title="User Management API",
    description="A FastAPI application with SQLite database",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """Initialize the database on application startup."""
    init_db()

app.include_router(users_router, prefix="/users", tags=["users"])

@app.get("/")
async def root():
    return {"message": "Welcome to User Management API"}
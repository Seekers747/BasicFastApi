from fastapi import FastAPI # type: ignore[reportMissingImports]
from fastapi.staticfiles import StaticFiles # type: ignore[reportMissingImports]
from fastapi.responses import FileResponse # type: ignore[reportMissingImports]
from .users import router as users_router
from .database import init_db  # pyright: ignore[reportMissingImports]

app = FastAPI()

# Initialize database tables on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# Mount static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include API routes
app.include_router(users_router, prefix="/users", tags=["users"])

# Serve the HTML page at root
@app.get("/")
async def read_root():
    return FileResponse("app/static/index.html")
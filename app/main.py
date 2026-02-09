from fastapi import FastAPI # type: ignore[reportMissingImports]
from users import router as users_router # pyright: ignore[reportMissingImports]

app = FastAPI()

app.include_router(users_router, prefix="/users", tags=["users"])

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import database
from app.core.config import config
from app.modules.auth.router import router as auth_router
from app.modules.user.router import router as user_router

@asynccontextmanager
async def life_span(app: FastAPI):
    yield
    await database.close()

app = FastAPI(title= config.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(user_router, prefix="/users", tags=["Users"])

@app.get("/")
def root():
    return {"message": "Hello, World!"}
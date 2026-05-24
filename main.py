
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import database
from app.core.config import config
from app.modules.auth.router import router as auth_router
from app.modules.user.router import router as user_router
from app.modules.document.router import router as document_router
from app.rag.vector_store import vector_store

@asynccontextmanager
async def life_span(app: FastAPI):
    await vector_store.ensure_collection_exists()
    yield
    await database.close()

app = FastAPI(title= config.APP_NAME, lifespan=life_span)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(document_router, prefix="/documents", tags=["Documents"])

@app.get("/")
def root():
    return {"message": "Hello, World!"}
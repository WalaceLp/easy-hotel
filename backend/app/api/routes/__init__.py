from fastapi import APIRouter

from app.api.routes import auth, perfis, usuarios

api_router = APIRouter(prefix="/api")
api_router.include_router(auth.router)
api_router.include_router(perfis.router)
api_router.include_router(usuarios.router)

__all__ = ["api_router"]

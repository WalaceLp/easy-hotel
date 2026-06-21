from fastapi import APIRouter

from app.api.routes import auth, hospedes, perfis, quartos, reservas, usuarios

api_router = APIRouter(prefix="/api")
api_router.include_router(auth.router)
api_router.include_router(perfis.router)
api_router.include_router(usuarios.router)
api_router.include_router(hospedes.router)
api_router.include_router(quartos.router_tipos)
api_router.include_router(quartos.router_status)
api_router.include_router(quartos.router_quartos)
api_router.include_router(reservas.router)

__all__ = ["api_router"]

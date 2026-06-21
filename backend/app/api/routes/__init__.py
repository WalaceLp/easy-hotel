from fastapi import APIRouter

from app.api.routes import auth, hospedes, pagamentos, perfis, quartos, relatorios, reservas, usuarios

api_router = APIRouter(prefix="/api")
api_router.include_router(auth.router)
api_router.include_router(perfis.router)
api_router.include_router(usuarios.router)
api_router.include_router(hospedes.router)
api_router.include_router(quartos.router_tipos)
api_router.include_router(quartos.router_status)
api_router.include_router(quartos.router_quartos)
api_router.include_router(reservas.router)
api_router.include_router(pagamentos.router_pagamentos)
api_router.include_router(pagamentos.router_metodos)
api_router.include_router(pagamentos.router_reserva_pagamentos)
api_router.include_router(relatorios.router)

__all__ = ["api_router"]

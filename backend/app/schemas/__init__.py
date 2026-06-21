from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.hospede import HospedeCreate, HospedeRead, HospedeUpdate
from app.schemas.perfil import PerfilRead
from app.schemas.quarto import (
    QuartoCreate,
    QuartoRead,
    QuartoStatusUpdate,
    QuartoUpdate,
    StatusQuartoRead,
    TipoQuartoCreate,
    TipoQuartoRead,
    TipoQuartoStatusUpdate,
    TipoQuartoUpdate,
)
from app.schemas.reserva import ReservaCreate, ReservaRead, ReservaUpdate
from app.schemas.usuario import UsuarioCreate, UsuarioRead, UsuarioStatusUpdate, UsuarioUpdate

__all__ = [
    "HospedeCreate",
    "HospedeRead",
    "HospedeUpdate",
    "LoginRequest",
    "PerfilRead",
    "QuartoCreate",
    "QuartoRead",
    "QuartoStatusUpdate",
    "QuartoUpdate",
    "ReservaCreate",
    "ReservaRead",
    "ReservaUpdate",
    "StatusQuartoRead",
    "TokenResponse",
    "TipoQuartoCreate",
    "TipoQuartoRead",
    "TipoQuartoStatusUpdate",
    "TipoQuartoUpdate",
    "UsuarioCreate",
    "UsuarioRead",
    "UsuarioStatusUpdate",
    "UsuarioUpdate",
]

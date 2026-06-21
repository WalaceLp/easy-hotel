from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.estadia import CheckInRequest, CheckOutRequest, EstadiaRead
from app.schemas.hospede import HospedeCreate, HospedeRead, HospedeUpdate
from app.schemas.pagamento import (
    MetodoPagamentoCreate,
    MetodoPagamentoRead,
    MetodoPagamentoStatusUpdate,
    MetodoPagamentoUpdate,
    PagamentoCreate,
    PagamentoRead,
)
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
    "CheckInRequest",
    "CheckOutRequest",
    "EstadiaRead",
    "HospedeRead",
    "HospedeUpdate",
    "LoginRequest",
    "MetodoPagamentoCreate",
    "MetodoPagamentoRead",
    "MetodoPagamentoStatusUpdate",
    "MetodoPagamentoUpdate",
    "PagamentoCreate",
    "PagamentoRead",
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

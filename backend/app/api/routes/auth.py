from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import UsuarioAtual
from app.database.session import get_db
from app.schemas import LoginRequest, TokenResponse, UsuarioRead
from app.services import AuthService

router = APIRouter(prefix="/auth", tags=["autenticação"])


@router.post("/login", response_model=TokenResponse)
def login(dados: LoginRequest, db: Annotated[Session, Depends(get_db)]) -> TokenResponse:
    token, usuario = AuthService(db).autenticar(dados.login, dados.senha)
    return TokenResponse(access_token=token, usuario=usuario)


@router.get("/me", response_model=UsuarioRead)
def me(usuario: UsuarioAtual) -> UsuarioRead:
    return usuario

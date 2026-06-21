from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import exigir_perfis
from app.database.session import get_db
from app.models import Usuario
from app.schemas import UsuarioCreate, UsuarioRead, UsuarioStatusUpdate, UsuarioUpdate
from app.services import UsuarioService

router = APIRouter(prefix="/usuarios", tags=["usuários"])

Administrador = Annotated[Usuario, Depends(exigir_perfis("ADMINISTRADOR"))]


@router.get("", response_model=list[UsuarioRead])
def listar_usuarios(
    db: Annotated[Session, Depends(get_db)],
    _: Administrador,
) -> list[Usuario]:
    return UsuarioService(db).listar()


@router.post("", response_model=UsuarioRead, status_code=201)
def criar_usuario(
    dados: UsuarioCreate,
    db: Annotated[Session, Depends(get_db)],
    _: Administrador,
) -> Usuario:
    return UsuarioService(db).criar(dados)


@router.get("/{usuario_id}", response_model=UsuarioRead)
def buscar_usuario(
    usuario_id: int,
    db: Annotated[Session, Depends(get_db)],
    _: Administrador,
) -> Usuario:
    return UsuarioService(db).buscar_por_id(usuario_id)


@router.put("/{usuario_id}", response_model=UsuarioRead)
def atualizar_usuario(
    usuario_id: int,
    dados: UsuarioUpdate,
    db: Annotated[Session, Depends(get_db)],
    _: Administrador,
) -> Usuario:
    return UsuarioService(db).atualizar(usuario_id, dados)


@router.patch("/{usuario_id}/status", response_model=UsuarioRead)
def atualizar_status_usuario(
    usuario_id: int,
    dados: UsuarioStatusUpdate,
    db: Annotated[Session, Depends(get_db)],
    _: Administrador,
) -> Usuario:
    return UsuarioService(db).atualizar_status(usuario_id, dados)

from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import UsuarioAtual, exigir_perfis
from app.database.session import get_db
from app.models import Usuario
from app.schemas import ReservaCreate, ReservaRead, ReservaUpdate
from app.services import ReservaService

router = APIRouter(prefix="/reservas", tags=["reservas"])

OperadorReservas = Annotated[
    Usuario,
    Depends(exigir_perfis("ADMINISTRADOR", "GERENTE", "RECEPCIONISTA")),
]


@router.get("", response_model=list[ReservaRead])
def listar_reservas(
    db: Annotated[Session, Depends(get_db)],
    _: OperadorReservas,
) -> list:
    return ReservaService(db).listar()


@router.post("", response_model=ReservaRead, status_code=status.HTTP_201_CREATED)
def criar_reserva(
    dados: ReservaCreate,
    db: Annotated[Session, Depends(get_db)],
    usuario: UsuarioAtual,
):
    return ReservaService(db).criar(dados, usuario)


@router.get("/{reserva_id}", response_model=ReservaRead)
def buscar_reserva(
    reserva_id: int,
    db: Annotated[Session, Depends(get_db)],
    _: OperadorReservas,
):
    return ReservaService(db).buscar_por_id(reserva_id)


@router.put("/{reserva_id}", response_model=ReservaRead)
def atualizar_reserva(
    reserva_id: int,
    dados: ReservaUpdate,
    db: Annotated[Session, Depends(get_db)],
    _: OperadorReservas,
):
    return ReservaService(db).atualizar(reserva_id, dados)


@router.patch("/{reserva_id}/confirmar", response_model=ReservaRead)
def confirmar_reserva(
    reserva_id: int,
    db: Annotated[Session, Depends(get_db)],
    _: OperadorReservas,
):
    return ReservaService(db).confirmar(reserva_id)


@router.patch("/{reserva_id}/cancelar", response_model=ReservaRead)
def cancelar_reserva(
    reserva_id: int,
    db: Annotated[Session, Depends(get_db)],
    _: OperadorReservas,
):
    return ReservaService(db).cancelar(reserva_id)

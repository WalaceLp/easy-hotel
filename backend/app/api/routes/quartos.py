from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import exigir_perfis
from app.database.session import get_db
from app.models import Usuario
from app.schemas import (
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
from app.services import QuartoService, TipoQuartoService

router_tipos = APIRouter(prefix="/tipos-quarto", tags=["tipos de quarto"])
router_quartos = APIRouter(prefix="/quartos", tags=["quartos"])
router_status = APIRouter(prefix="/status-quarto", tags=["status de quarto"])

GestorQuartos = Annotated[Usuario, Depends(exigir_perfis("ADMINISTRADOR", "GERENTE"))]
LeitorQuartos = Annotated[
    Usuario,
    Depends(exigir_perfis("ADMINISTRADOR", "GERENTE", "RECEPCIONISTA")),
]


@router_tipos.get("", response_model=list[TipoQuartoRead])
def listar_tipos_quarto(db: Annotated[Session, Depends(get_db)], _: LeitorQuartos) -> list:
    return TipoQuartoService(db).listar()


@router_tipos.post("", response_model=TipoQuartoRead, status_code=status.HTTP_201_CREATED)
def criar_tipo_quarto(
    dados: TipoQuartoCreate,
    db: Annotated[Session, Depends(get_db)],
    _: GestorQuartos,
):
    return TipoQuartoService(db).criar(dados)


@router_tipos.get("/{tipo_id}", response_model=TipoQuartoRead)
def buscar_tipo_quarto(tipo_id: int, db: Annotated[Session, Depends(get_db)], _: LeitorQuartos):
    return TipoQuartoService(db).buscar_por_id(tipo_id)


@router_tipos.put("/{tipo_id}", response_model=TipoQuartoRead)
def atualizar_tipo_quarto(
    tipo_id: int,
    dados: TipoQuartoUpdate,
    db: Annotated[Session, Depends(get_db)],
    _: GestorQuartos,
):
    return TipoQuartoService(db).atualizar(tipo_id, dados)


@router_tipos.patch("/{tipo_id}/status", response_model=TipoQuartoRead)
def atualizar_status_tipo_quarto(
    tipo_id: int,
    dados: TipoQuartoStatusUpdate,
    db: Annotated[Session, Depends(get_db)],
    _: GestorQuartos,
):
    return TipoQuartoService(db).atualizar_status(tipo_id, dados)


@router_status.get("", response_model=list[StatusQuartoRead])
def listar_status_quarto(db: Annotated[Session, Depends(get_db)], _: LeitorQuartos) -> list:
    return QuartoService(db).listar_status()


@router_quartos.get("", response_model=list[QuartoRead])
def listar_quartos(db: Annotated[Session, Depends(get_db)], _: LeitorQuartos) -> list:
    return QuartoService(db).listar()


@router_quartos.post("", response_model=QuartoRead, status_code=status.HTTP_201_CREATED)
def criar_quarto(
    dados: QuartoCreate,
    db: Annotated[Session, Depends(get_db)],
    _: GestorQuartos,
):
    return QuartoService(db).criar(dados)


@router_quartos.get("/disponiveis", response_model=list[QuartoRead])
def listar_quartos_disponiveis(
    db: Annotated[Session, Depends(get_db)],
    _: LeitorQuartos,
    data_entrada: date = Query(...),
    data_saida: date = Query(...),
) -> list:
    return QuartoService(db).listar_disponiveis(data_entrada, data_saida)


@router_quartos.get("/{numero}", response_model=QuartoRead)
def buscar_quarto(numero: str, db: Annotated[Session, Depends(get_db)], _: LeitorQuartos):
    return QuartoService(db).buscar_por_numero(numero)


@router_quartos.put("/{numero}", response_model=QuartoRead)
def atualizar_quarto(
    numero: str,
    dados: QuartoUpdate,
    db: Annotated[Session, Depends(get_db)],
    _: GestorQuartos,
):
    return QuartoService(db).atualizar(numero, dados)


@router_quartos.patch("/{numero}/status", response_model=QuartoRead)
def atualizar_status_quarto(
    numero: str,
    dados: QuartoStatusUpdate,
    db: Annotated[Session, Depends(get_db)],
    _: GestorQuartos,
):
    return QuartoService(db).atualizar_status(numero, dados)

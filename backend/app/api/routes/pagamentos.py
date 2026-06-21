from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import UsuarioAtual, exigir_perfis
from app.database.session import get_db
from app.models import Usuario
from app.schemas import (
    MetodoPagamentoCreate,
    MetodoPagamentoRead,
    MetodoPagamentoStatusUpdate,
    MetodoPagamentoUpdate,
    PagamentoCreate,
    PagamentoRead,
)
from app.services import MetodoPagamentoService, PagamentoService

router_pagamentos = APIRouter(prefix="/pagamentos", tags=["pagamentos"])
router_metodos = APIRouter(prefix="/metodos-pagamento", tags=["métodos de pagamento"])
router_reserva_pagamentos = APIRouter(prefix="/reservas", tags=["pagamentos"])

Financeiro = Annotated[Usuario, Depends(exigir_perfis("ADMINISTRADOR", "GERENTE"))]
OperadorPagamento = Annotated[
    Usuario,
    Depends(exigir_perfis("ADMINISTRADOR", "GERENTE", "RECEPCIONISTA")),
]


@router_pagamentos.get("", response_model=list[PagamentoRead])
def listar_pagamentos(
    db: Annotated[Session, Depends(get_db)],
    _: Financeiro,
) -> list:
    return PagamentoService(db).listar()


@router_pagamentos.post("", response_model=PagamentoRead, status_code=status.HTTP_201_CREATED)
def criar_pagamento(
    dados: PagamentoCreate,
    db: Annotated[Session, Depends(get_db)],
    usuario: UsuarioAtual,
) -> object:
    return PagamentoService(db).criar(dados, usuario)


@router_pagamentos.get("/{pagamento_id}", response_model=PagamentoRead)
def buscar_pagamento(
    pagamento_id: int,
    db: Annotated[Session, Depends(get_db)],
    _: Financeiro,
) -> object:
    return PagamentoService(db).buscar_por_id(pagamento_id)


@router_reserva_pagamentos.get("/{reserva_id}/pagamentos", response_model=list[PagamentoRead])
def listar_pagamentos_reserva(
    reserva_id: int,
    db: Annotated[Session, Depends(get_db)],
    _: OperadorPagamento,
) -> list:
    return PagamentoService(db).listar_por_reserva(reserva_id)


@router_metodos.get("", response_model=list[MetodoPagamentoRead])
def listar_metodos_pagamento(
    db: Annotated[Session, Depends(get_db)],
    _: OperadorPagamento,
) -> list:
    return MetodoPagamentoService(db).listar()


@router_metodos.post("", response_model=MetodoPagamentoRead, status_code=status.HTTP_201_CREATED)
def criar_metodo_pagamento(
    dados: MetodoPagamentoCreate,
    db: Annotated[Session, Depends(get_db)],
    _: Financeiro,
) -> object:
    return MetodoPagamentoService(db).criar(dados)


@router_metodos.put("/{metodo_id}", response_model=MetodoPagamentoRead)
def atualizar_metodo_pagamento(
    metodo_id: int,
    dados: MetodoPagamentoUpdate,
    db: Annotated[Session, Depends(get_db)],
    _: Financeiro,
) -> object:
    return MetodoPagamentoService(db).atualizar(metodo_id, dados)


@router_metodos.patch("/{metodo_id}/status", response_model=MetodoPagamentoRead)
def atualizar_status_metodo_pagamento(
    metodo_id: int,
    dados: MetodoPagamentoStatusUpdate,
    db: Annotated[Session, Depends(get_db)],
    _: Financeiro,
) -> object:
    return MetodoPagamentoService(db).atualizar_status(metodo_id, dados)

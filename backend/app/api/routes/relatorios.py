from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.dependencies import exigir_perfis
from app.database.session import get_db
from app.models import Usuario
from app.schemas.relatorio import (
    DashboardResponse,
    FaturamentoResponse,
    OcupacaoResponse,
    ReservasRelatorioResponse,
)
from app.services import RelatorioService

router = APIRouter(prefix="/relatorios", tags=["relatórios"])

GestorRelatorios = Annotated[Usuario, Depends(exigir_perfis("ADMINISTRADOR", "GERENTE"))]


@router.get("/dashboard", response_model=DashboardResponse)
def dashboard(
    db: Annotated[Session, Depends(get_db)],
    _: GestorRelatorios,
) -> DashboardResponse:
    return RelatorioService(db).dashboard()


@router.get("/ocupacao", response_model=OcupacaoResponse)
def ocupacao(
    db: Annotated[Session, Depends(get_db)],
    _: GestorRelatorios,
    data_inicio: date | None = Query(default=None),
    data_fim: date | None = Query(default=None),
) -> OcupacaoResponse:
    return RelatorioService(db).ocupacao(data_inicio, data_fim)


@router.get("/faturamento", response_model=FaturamentoResponse)
def faturamento(
    db: Annotated[Session, Depends(get_db)],
    _: GestorRelatorios,
    data_inicio: date | None = Query(default=None),
    data_fim: date | None = Query(default=None),
) -> FaturamentoResponse:
    return RelatorioService(db).faturamento(data_inicio, data_fim)


@router.get("/reservas", response_model=ReservasRelatorioResponse)
def reservas(
    db: Annotated[Session, Depends(get_db)],
    _: GestorRelatorios,
    data_inicio: date | None = Query(default=None),
    data_fim: date | None = Query(default=None),
) -> ReservasRelatorioResponse:
    return RelatorioService(db).reservas(data_inicio, data_fim)

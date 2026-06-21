from datetime import date
from decimal import Decimal

from pydantic import BaseModel

from app.schemas.reserva import ReservaRead


class DashboardResponse(BaseModel):
    total_hospedes: int
    quartos_disponiveis: int
    quartos_ocupados: int
    reservas_pendentes: int
    reservas_confirmadas: int
    checkins_previstos_hoje: int
    checkouts_previstos_hoje: int
    faturamento_mes: Decimal
    taxa_ocupacao: float
    reservas_recentes: list[ReservaRead]


class OcupacaoResponse(BaseModel):
    data_inicio: date | None
    data_fim: date | None
    total_quartos_ativos: int
    quartos_ocupados: int
    taxa_ocupacao: float


class FaturamentoResponse(BaseModel):
    data_inicio: date | None
    data_fim: date | None
    valor_total: Decimal
    quantidade_pagamentos: int


class ReservasRelatorioResponse(BaseModel):
    data_inicio: date | None
    data_fim: date | None
    total: int
    pendentes: int
    confirmadas: int
    em_andamento: int
    concluidas: int
    canceladas: int

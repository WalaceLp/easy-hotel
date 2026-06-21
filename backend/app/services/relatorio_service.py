from datetime import date

from sqlalchemy.orm import Session

from app.repositories import RelatorioRepository, ReservaRepository
from app.schemas.relatorio import (
    DashboardResponse,
    FaturamentoResponse,
    OcupacaoResponse,
    ReservasRelatorioResponse,
)


class RelatorioService:
    def __init__(self, db: Session) -> None:
        self.relatorio_repository = RelatorioRepository(db)
        self.reserva_repository = ReservaRepository(db)

    def dashboard(self) -> DashboardResponse:
        hoje = date.today()
        inicio_mes = hoje.replace(day=1)
        faturamento_mes, _ = self.relatorio_repository.faturamento(inicio_mes, hoje)
        quartos_ativos = self.relatorio_repository.contar_quartos_ativos()
        quartos_ocupados = self.relatorio_repository.contar_quartos_por_status("OCUPADO")
        return DashboardResponse(
            total_hospedes=self.relatorio_repository.contar_hospedes(),
            quartos_disponiveis=self.relatorio_repository.contar_quartos_por_status("DISPONIVEL"),
            quartos_ocupados=quartos_ocupados,
            reservas_pendentes=self.relatorio_repository.contar_reservas_por_status("PENDENTE"),
            reservas_confirmadas=self.relatorio_repository.contar_reservas_por_status("CONFIRMADA"),
            checkins_previstos_hoje=self.relatorio_repository.contar_checkins_previstos(hoje),
            checkouts_previstos_hoje=self.relatorio_repository.contar_checkouts_previstos(hoje),
            faturamento_mes=faturamento_mes,
            taxa_ocupacao=self._calcular_taxa(quartos_ocupados, quartos_ativos),
            reservas_recentes=self.reserva_repository.listar()[:5],
        )

    def ocupacao(self, data_inicio: date | None, data_fim: date | None) -> OcupacaoResponse:
        total_quartos = self.relatorio_repository.contar_quartos_ativos()
        ocupados = self.relatorio_repository.quartos_ocupados_periodo(data_inicio, data_fim)
        return OcupacaoResponse(
            data_inicio=data_inicio,
            data_fim=data_fim,
            total_quartos_ativos=total_quartos,
            quartos_ocupados=ocupados,
            taxa_ocupacao=self._calcular_taxa(ocupados, total_quartos),
        )

    def faturamento(self, data_inicio: date | None, data_fim: date | None) -> FaturamentoResponse:
        valor_total, quantidade = self.relatorio_repository.faturamento(data_inicio, data_fim)
        return FaturamentoResponse(
            data_inicio=data_inicio,
            data_fim=data_fim,
            valor_total=valor_total,
            quantidade_pagamentos=quantidade,
        )

    def reservas(self, data_inicio: date | None, data_fim: date | None) -> ReservasRelatorioResponse:
        return ReservasRelatorioResponse(
            data_inicio=data_inicio,
            data_fim=data_fim,
            total=self.relatorio_repository.contar_reservas(data_inicio, data_fim),
            pendentes=self.relatorio_repository.contar_reservas_por_status("PENDENTE", data_inicio, data_fim),
            confirmadas=self.relatorio_repository.contar_reservas_por_status("CONFIRMADA", data_inicio, data_fim),
            em_andamento=self.relatorio_repository.contar_reservas_por_status("EM_ANDAMENTO", data_inicio, data_fim),
            concluidas=self.relatorio_repository.contar_reservas_por_status("CONCLUIDA", data_inicio, data_fim),
            canceladas=self.relatorio_repository.contar_reservas_por_status("CANCELADA", data_inicio, data_fim),
        )

    def _calcular_taxa(self, ocupados: int, total: int) -> float:
        if total == 0:
            return 0.0
        return round((ocupados / total) * 100, 2)

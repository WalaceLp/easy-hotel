from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Estadia, Hospede, Pagamento, Quarto, Reserva, StatusQuarto


class RelatorioRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def contar_hospedes(self) -> int:
        return self._contar(select(func.count(Hospede.id)))

    def contar_quartos_por_status(self, descricao: str) -> int:
        stmt = select(func.count(Quarto.numero)).join(StatusQuarto).where(StatusQuarto.descricao == descricao)
        return self._contar(stmt)

    def contar_quartos_ativos(self) -> int:
        return self._contar(select(func.count(Quarto.numero)).where(Quarto.ativo.is_(True)))

    def contar_reservas_por_status(self, status: str, data_inicio: date | None = None, data_fim: date | None = None) -> int:
        stmt = select(func.count(Reserva.id)).where(Reserva.status == status)
        stmt = self._filtrar_periodo_reserva(stmt, data_inicio, data_fim)
        return self._contar(stmt)

    def contar_checkins_previstos(self, data_ref: date) -> int:
        stmt = select(func.count(Reserva.id)).where(
            Reserva.data_entrada == data_ref,
            Reserva.status == "CONFIRMADA",
        )
        return self._contar(stmt)

    def contar_checkouts_previstos(self, data_ref: date) -> int:
        stmt = select(func.count(Reserva.id)).where(
            Reserva.data_saida == data_ref,
            Reserva.status == "EM_ANDAMENTO",
        )
        return self._contar(stmt)

    def faturamento(self, data_inicio: date | None = None, data_fim: date | None = None) -> tuple[Decimal, int]:
        stmt = select(func.coalesce(func.sum(Pagamento.valor), 0), func.count(Pagamento.id))
        if data_inicio is not None:
            stmt = stmt.where(func.date(Pagamento.data_pagamento) >= data_inicio)
        if data_fim is not None:
            stmt = stmt.where(func.date(Pagamento.data_pagamento) <= data_fim)
        valor, quantidade = self.db.execute(stmt).one()
        return Decimal(valor or 0), int(quantidade or 0)

    def reservas_recentes(self, limite: int = 5) -> list[Reserva]:
        stmt = select(Reserva).order_by(Reserva.criado_em.desc(), Reserva.id.desc()).limit(limite)
        return list(self.db.scalars(stmt).all())

    def quartos_ocupados_periodo(self, data_inicio: date | None = None, data_fim: date | None = None) -> int:
        stmt = select(func.count(func.distinct(Estadia.reserva_id))).join(Reserva)
        if data_inicio is not None:
            stmt = stmt.where(Reserva.data_saida >= data_inicio)
        if data_fim is not None:
            stmt = stmt.where(Reserva.data_entrada <= data_fim)
        return self._contar(stmt)

    def contar_reservas(self, data_inicio: date | None = None, data_fim: date | None = None) -> int:
        stmt = self._filtrar_periodo_reserva(select(func.count(Reserva.id)), data_inicio, data_fim)
        return self._contar(stmt)

    def _contar(self, stmt) -> int:
        return int(self.db.scalar(stmt) or 0)

    def _filtrar_periodo_reserva(self, stmt, data_inicio: date | None, data_fim: date | None):
        if data_inicio is not None:
            stmt = stmt.where(Reserva.data_entrada >= data_inicio)
        if data_fim is not None:
            stmt = stmt.where(Reserva.data_entrada <= data_fim)
        return stmt

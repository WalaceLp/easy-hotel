from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.models import MetodoPagamento, Pagamento


class MetodoPagamentoRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def listar(self) -> list[MetodoPagamento]:
        return list(self.db.scalars(select(MetodoPagamento).order_by(MetodoPagamento.descricao)).all())

    def buscar_por_id(self, metodo_id: int) -> MetodoPagamento | None:
        return self.db.get(MetodoPagamento, metodo_id)

    def existe_descricao(self, descricao: str, ignorar_metodo_id: int | None = None) -> bool:
        stmt = select(MetodoPagamento.id).where(MetodoPagamento.descricao == descricao)
        if ignorar_metodo_id is not None:
            stmt = stmt.where(MetodoPagamento.id != ignorar_metodo_id)
        return self.db.scalar(stmt) is not None

    def adicionar(self, metodo: MetodoPagamento) -> MetodoPagamento:
        self.db.add(metodo)
        self.db.flush()
        self.db.refresh(metodo)
        return metodo

    def salvar(self) -> None:
        self.db.commit()


class PagamentoRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def listar(self) -> list[Pagamento]:
        stmt = select(Pagamento).options(joinedload(Pagamento.metodo)).order_by(Pagamento.data_pagamento.desc())
        return list(self.db.scalars(stmt).all())

    def buscar_por_id(self, pagamento_id: int) -> Pagamento | None:
        stmt = select(Pagamento).options(joinedload(Pagamento.metodo)).where(Pagamento.id == pagamento_id)
        return self.db.scalar(stmt)

    def listar_por_reserva(self, reserva_id: int) -> list[Pagamento]:
        stmt = (
            select(Pagamento)
            .options(joinedload(Pagamento.metodo))
            .where(Pagamento.reserva_id == reserva_id)
            .order_by(Pagamento.data_pagamento.desc())
        )
        return list(self.db.scalars(stmt).all())

    def total_por_reserva(self, reserva_id: int) -> Decimal:
        total = self.db.scalar(select(func.coalesce(func.sum(Pagamento.valor), 0)).where(Pagamento.reserva_id == reserva_id))
        return Decimal(total or 0)

    def adicionar(self, pagamento: Pagamento) -> Pagamento:
        self.db.add(pagamento)
        self.db.flush()
        return self.buscar_por_id(pagamento.id) or pagamento

    def salvar(self) -> None:
        self.db.commit()

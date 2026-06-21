from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import Quarto, Reserva, Usuario
from app.repositories.quarto_repository import STATUS_RESERVAS_BLOQUEANTES


class ReservaRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def listar(self) -> list[Reserva]:
        stmt = (
            select(Reserva)
            .options(
                joinedload(Reserva.hospede),
                joinedload(Reserva.quarto).joinedload(Quarto.tipo),
                joinedload(Reserva.quarto).joinedload(Quarto.status),
                joinedload(Reserva.usuario).joinedload(Usuario.perfil),
            )
            .order_by(Reserva.data_entrada.desc(), Reserva.id.desc())
        )
        return list(self.db.scalars(stmt).all())

    def buscar_por_id(self, reserva_id: int) -> Reserva | None:
        stmt = (
            select(Reserva)
            .options(
                joinedload(Reserva.hospede),
                joinedload(Reserva.quarto).joinedload(Quarto.tipo),
                joinedload(Reserva.quarto).joinedload(Quarto.status),
                joinedload(Reserva.usuario).joinedload(Usuario.perfil),
            )
            .where(Reserva.id == reserva_id)
        )
        return self.db.scalar(stmt)

    def existe_conflito(
        self,
        quarto_numero: str,
        data_entrada: date,
        data_saida: date,
        ignorar_reserva_id: int | None = None,
    ) -> bool:
        stmt = select(Reserva.id).where(
            Reserva.quarto_numero == quarto_numero,
            Reserva.status.in_(STATUS_RESERVAS_BLOQUEANTES),
            Reserva.data_entrada < data_saida,
            Reserva.data_saida > data_entrada,
        )
        if ignorar_reserva_id is not None:
            stmt = stmt.where(Reserva.id != ignorar_reserva_id)
        return self.db.scalar(stmt) is not None

    def adicionar(self, reserva: Reserva) -> Reserva:
        self.db.add(reserva)
        self.db.flush()
        return self.buscar_por_id(reserva.id) or reserva

    def salvar(self) -> None:
        self.db.commit()

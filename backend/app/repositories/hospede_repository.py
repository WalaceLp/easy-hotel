from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Hospede, Reserva


class HospedeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def listar(self) -> list[Hospede]:
        return list(self.db.scalars(select(Hospede).order_by(Hospede.nome)).all())

    def buscar_por_id(self, hospede_id: int) -> Hospede | None:
        return self.db.get(Hospede, hospede_id)

    def buscar_por_cpf(self, cpf: str) -> Hospede | None:
        return self.db.scalar(select(Hospede).where(Hospede.cpf == cpf))

    def existe_cpf(self, cpf: str, ignorar_hospede_id: int | None = None) -> bool:
        stmt = select(Hospede.id).where(Hospede.cpf == cpf)
        if ignorar_hospede_id is not None:
            stmt = stmt.where(Hospede.id != ignorar_hospede_id)
        return self.db.scalar(stmt) is not None

    def possui_reservas(self, hospede_id: int) -> bool:
        return self.db.scalar(select(Reserva.id).where(Reserva.hospede_id == hospede_id)) is not None

    def adicionar(self, hospede: Hospede) -> Hospede:
        self.db.add(hospede)
        self.db.flush()
        self.db.refresh(hospede)
        return hospede

    def excluir(self, hospede: Hospede) -> None:
        self.db.delete(hospede)

    def salvar(self) -> None:
        self.db.commit()

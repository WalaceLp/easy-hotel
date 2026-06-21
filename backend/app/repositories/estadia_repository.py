from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Estadia


class EstadiaRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def buscar_por_reserva_id(self, reserva_id: int) -> Estadia | None:
        return self.db.scalar(select(Estadia).where(Estadia.reserva_id == reserva_id))

    def adicionar(self, estadia: Estadia) -> Estadia:
        self.db.add(estadia)
        self.db.flush()
        self.db.refresh(estadia)
        return estadia

    def salvar(self) -> None:
        self.db.commit()

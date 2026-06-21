from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Perfil


class PerfilRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def listar(self) -> list[Perfil]:
        return list(self.db.scalars(select(Perfil).order_by(Perfil.nome)).all())

    def buscar_por_id(self, perfil_id: int) -> Perfil | None:
        return self.db.get(Perfil, perfil_id)

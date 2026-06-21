from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import Usuario


class UsuarioRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def listar(self) -> list[Usuario]:
        stmt = select(Usuario).options(joinedload(Usuario.perfil)).order_by(Usuario.nome)
        return list(self.db.scalars(stmt).all())

    def buscar_por_id(self, usuario_id: int) -> Usuario | None:
        stmt = select(Usuario).options(joinedload(Usuario.perfil)).where(Usuario.id == usuario_id)
        return self.db.scalar(stmt)

    def buscar_por_login(self, login: str) -> Usuario | None:
        stmt = select(Usuario).options(joinedload(Usuario.perfil)).where(Usuario.login == login)
        return self.db.scalar(stmt)

    def existe_login(self, login: str, ignorar_usuario_id: int | None = None) -> bool:
        stmt = select(Usuario.id).where(Usuario.login == login)
        if ignorar_usuario_id is not None:
            stmt = stmt.where(Usuario.id != ignorar_usuario_id)
        return self.db.scalar(stmt) is not None

    def adicionar(self, usuario: Usuario) -> Usuario:
        self.db.add(usuario)
        self.db.flush()
        self.db.refresh(usuario, attribute_names=["perfil"])
        return usuario

    def salvar(self) -> None:
        self.db.commit()

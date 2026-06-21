from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import gerar_hash_senha
from app.database.session import SessionLocal
from app.models import Perfil, Quarto, StatusQuarto, TipoQuarto, Usuario


def obter_ou_criar(db: Session, modelo, defaults: dict | None = None, **filtros):
    registro = db.scalar(select(modelo).filter_by(**filtros))
    if registro:
        return registro

    valores = {**filtros, **(defaults or {})}
    registro = modelo(**valores)
    db.add(registro)
    db.flush()
    return registro


def seed() -> None:
    with SessionLocal() as db:
        administrador = obter_ou_criar(db, Perfil, nome="ADMINISTRADOR")
        obter_ou_criar(db, Perfil, nome="GERENTE")
        obter_ou_criar(db, Perfil, nome="RECEPCIONISTA")

        disponivel = obter_ou_criar(db, StatusQuarto, descricao="DISPONIVEL")
        for status in ["RESERVADO", "OCUPADO", "MANUTENCAO", "INATIVO"]:
            obter_ou_criar(db, StatusQuarto, descricao=status)

        solteiro = obter_ou_criar(
            db, TipoQuarto, descricao="Solteiro", defaults={"preco_base": 120.00, "capacidade": 1}
        )
        casal = obter_ou_criar(
            db, TipoQuarto, descricao="Casal", defaults={"preco_base": 180.00, "capacidade": 2}
        )
        familia = obter_ou_criar(
            db, TipoQuarto, descricao="Familia", defaults={"preco_base": 260.00, "capacidade": 4}
        )

        for numero, tipo in [("101", solteiro), ("102", solteiro), ("201", casal), ("202", casal), ("301", familia)]:
            obter_ou_criar(
                db,
                Quarto,
                numero=numero,
                defaults={"tipo_id": tipo.id, "status_id": disponivel.id, "ativo": True},
            )

        usuario_admin = db.scalar(select(Usuario).where(Usuario.login == settings.admin_default_login))
        if not usuario_admin:
            db.add(
                Usuario(
                    nome=settings.admin_default_name,
                    login=settings.admin_default_login,
                    senha_hash=gerar_hash_senha(settings.admin_default_password),
                    perfil_id=administrador.id,
                    ativo=True,
                )
            )

        db.commit()


if __name__ == "__main__":
    seed()

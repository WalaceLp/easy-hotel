from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.security import gerar_hash_senha
from app.database.base import Base
from app.database.session import get_db
from app.main import app
from app.models import MetodoPagamento, Perfil, Quarto, StatusQuarto, TipoQuarto, Usuario


@pytest.fixture()
def db() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    with TestingSessionLocal() as session:
        administrador = Perfil(nome="ADMINISTRADOR")
        gerente = Perfil(nome="GERENTE")
        recepcionista = Perfil(nome="RECEPCIONISTA")
        session.add_all([administrador, gerente, recepcionista])
        session.flush()

        disponivel = StatusQuarto(descricao="DISPONIVEL")
        reservado = StatusQuarto(descricao="RESERVADO")
        ocupado = StatusQuarto(descricao="OCUPADO")
        manutencao = StatusQuarto(descricao="MANUTENCAO")
        inativo = StatusQuarto(descricao="INATIVO")
        session.add_all([disponivel, reservado, ocupado, manutencao, inativo])
        session.flush()

        solteiro = TipoQuarto(descricao="Solteiro", preco_base=120, capacidade=1, ativo=True)
        casal = TipoQuarto(descricao="Casal", preco_base=180, capacidade=2, ativo=True)
        session.add_all([solteiro, casal])
        session.flush()

        session.add_all(
            [
                Quarto(numero="101", tipo_id=solteiro.id, status_id=disponivel.id, ativo=True),
                Quarto(numero="201", tipo_id=casal.id, status_id=disponivel.id, ativo=True),
                Quarto(numero="301", tipo_id=casal.id, status_id=manutencao.id, ativo=True),
            ]
        )
        session.add_all(
            [
                MetodoPagamento(descricao="DINHEIRO", ativo=True),
                MetodoPagamento(descricao="PIX", ativo=True),
                MetodoPagamento(descricao="CARTAO_CREDITO", ativo=True),
                MetodoPagamento(descricao="CARTAO_DEBITO", ativo=True),
            ]
        )

        session.add_all(
            [
                Usuario(
                    nome="Administrador",
                    login="admin",
                    senha_hash=gerar_hash_senha("admin123"),
                    perfil_id=administrador.id,
                    ativo=True,
                ),
                Usuario(
                    nome="Recepcionista",
                    login="recepcao",
                    senha_hash=gerar_hash_senha("recepcao123"),
                    perfil_id=recepcionista.id,
                    ativo=True,
                ),
                Usuario(
                    nome="Inativo",
                    login="inativo",
                    senha_hash=gerar_hash_senha("inativo123"),
                    perfil_id=gerente.id,
                    ativo=False,
                ),
            ]
        )
        session.commit()
        yield session

    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db: Session) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

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
from app.models import Perfil, Usuario


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

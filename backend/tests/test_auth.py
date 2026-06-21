from fastapi.testclient import TestClient


def autenticar(client: TestClient, login: str = "admin", senha: str = "admin123") -> str:
    response = client.post("/api/auth/login", json={"login": login, "senha": senha})
    assert response.status_code == 200
    return response.json()["access_token"]


def test_login_retorna_token_e_usuario(client: TestClient) -> None:
    response = client.post("/api/auth/login", json={"login": "admin", "senha": "admin123"})

    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["access_token"]
    assert data["usuario"]["login"] == "admin"
    assert data["usuario"]["perfil"]["nome"] == "ADMINISTRADOR"
    assert "senha_hash" not in data["usuario"]


def test_login_com_senha_invalida_retorna_401(client: TestClient) -> None:
    response = client.post("/api/auth/login", json={"login": "admin", "senha": "errada"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Login ou senha inválidos."


def test_usuario_inativo_nao_realiza_login(client: TestClient) -> None:
    response = client.post("/api/auth/login", json={"login": "inativo", "senha": "inativo123"})

    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário inativo não pode realizar login."


def test_me_retorna_usuario_autenticado(client: TestClient) -> None:
    token = autenticar(client)

    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()["login"] == "admin"


def test_me_sem_token_retorna_401(client: TestClient) -> None:
    response = client.get("/api/auth/me")

    assert response.status_code == 401
    assert response.json()["detail"] == "Token de autenticação não informado."


def test_recepcionista_nao_lista_usuarios(client: TestClient) -> None:
    token = autenticar(client, login="recepcao", senha="recepcao123")

    response = client.get("/api/usuarios", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 403
    assert response.json()["detail"] == "Usuário não possui permissão para acessar este recurso."


def test_administrador_cria_usuario(client: TestClient) -> None:
    token = autenticar(client)

    response = client.post(
        "/api/usuarios",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome": "Gerente Teste",
            "login": "gerente",
            "senha": "gerente123",
            "perfil_id": 2,
            "ativo": True,
        },
    )

    assert response.status_code == 201
    assert response.json()["login"] == "gerente"
    assert response.json()["perfil"]["nome"] == "GERENTE"


def test_nao_cria_usuario_com_login_duplicado(client: TestClient) -> None:
    token = autenticar(client)

    response = client.post(
        "/api/usuarios",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nome": "Outro Admin",
            "login": "admin",
            "senha": "admin456",
            "perfil_id": 1,
            "ativo": True,
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Já existe usuário cadastrado com este login."

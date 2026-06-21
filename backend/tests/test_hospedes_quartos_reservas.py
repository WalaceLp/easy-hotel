from datetime import date, timedelta

from fastapi.testclient import TestClient


def autenticar(client: TestClient, login: str = "admin", senha: str = "admin123") -> dict[str, str]:
    response = client.post("/api/auth/login", json={"login": login, "senha": senha})
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def criar_hospede(client: TestClient, headers: dict[str, str], cpf: str = "52998224725") -> int:
    response = client.post(
        "/api/hospedes",
        headers=headers,
        json={
            "nome": "Maria Silva",
            "cpf": cpf,
            "telefone": "11999999999",
            "email": "maria@example.com",
        },
    )
    assert response.status_code == 201
    return int(response.json()["id"])


def periodo() -> tuple[date, date]:
    entrada = date.today() + timedelta(days=10)
    saida = entrada + timedelta(days=3)
    return entrada, saida


def test_cadastra_hospede_com_cpf_valido(client: TestClient) -> None:
    headers = autenticar(client, login="recepcao", senha="recepcao123")

    response = client.post(
        "/api/hospedes",
        headers=headers,
        json={"nome": "Maria Silva", "cpf": "529.982.247-25", "telefone": None, "email": None},
    )

    assert response.status_code == 201
    assert response.json()["cpf"] == "52998224725"


def test_nao_cadastra_hospede_com_cpf_invalido(client: TestClient) -> None:
    headers = autenticar(client)

    response = client.post(
        "/api/hospedes",
        headers=headers,
        json={"nome": "Maria Silva", "cpf": "11111111111", "telefone": None, "email": None},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "CPF inválido."


def test_nao_cadastra_hospede_com_cpf_duplicado(client: TestClient) -> None:
    headers = autenticar(client)
    criar_hospede(client, headers)

    response = client.post(
        "/api/hospedes",
        headers=headers,
        json={"nome": "Outra Pessoa", "cpf": "52998224725", "telefone": None, "email": None},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Já existe hóspede cadastrado com este CPF."


def test_lista_quartos_disponiveis(client: TestClient) -> None:
    headers = autenticar(client, login="recepcao", senha="recepcao123")
    entrada, saida = periodo()

    response = client.get(
        "/api/quartos/disponiveis",
        headers=headers,
        params={"data_entrada": entrada.isoformat(), "data_saida": saida.isoformat()},
    )

    assert response.status_code == 200
    numeros = {quarto["numero"] for quarto in response.json()}
    assert {"101", "201"}.issubset(numeros)
    assert "301" not in numeros


def test_cria_reserva_calculando_valor_total(client: TestClient) -> None:
    headers = autenticar(client)
    hospede_id = criar_hospede(client, headers)
    entrada, saida = periodo()

    response = client.post(
        "/api/reservas",
        headers=headers,
        json={
            "data_entrada": entrada.isoformat(),
            "data_saida": saida.isoformat(),
            "quantidade_hospedes": 1,
            "hospede_id": hospede_id,
            "quarto_numero": "101",
            "observacoes": "Reserva de teste",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "PENDENTE"
    assert data["valor_total"] == "360.00"


def test_nao_cria_reserva_com_conflito_de_datas(client: TestClient) -> None:
    headers = autenticar(client)
    hospede_id = criar_hospede(client, headers)
    entrada, saida = periodo()
    payload = {
        "data_entrada": entrada.isoformat(),
        "data_saida": saida.isoformat(),
        "quantidade_hospedes": 1,
        "hospede_id": hospede_id,
        "quarto_numero": "101",
        "observacoes": None,
    }
    primeira = client.post("/api/reservas", headers=headers, json=payload)
    assert primeira.status_code == 201

    response = client.post("/api/reservas", headers=headers, json=payload)

    assert response.status_code == 409
    assert response.json()["detail"] == "Já existe reserva para este quarto no período informado."


def test_cancelada_nao_bloqueia_disponibilidade(client: TestClient) -> None:
    headers = autenticar(client)
    hospede_id = criar_hospede(client, headers)
    entrada, saida = periodo()
    response = client.post(
        "/api/reservas",
        headers=headers,
        json={
            "data_entrada": entrada.isoformat(),
            "data_saida": saida.isoformat(),
            "quantidade_hospedes": 1,
            "hospede_id": hospede_id,
            "quarto_numero": "101",
            "observacoes": None,
        },
    )
    assert response.status_code == 201
    reserva_id = response.json()["id"]
    cancelamento = client.patch(f"/api/reservas/{reserva_id}/cancelar", headers=headers)
    assert cancelamento.status_code == 200

    nova_reserva = client.post(
        "/api/reservas",
        headers=headers,
        json={
            "data_entrada": entrada.isoformat(),
            "data_saida": saida.isoformat(),
            "quantidade_hospedes": 1,
            "hospede_id": hospede_id,
            "quarto_numero": "101",
            "observacoes": None,
        },
    )

    assert nova_reserva.status_code == 201


def test_nao_reserva_quarto_em_manutencao(client: TestClient) -> None:
    headers = autenticar(client)
    hospede_id = criar_hospede(client, headers)
    entrada, saida = periodo()

    response = client.post(
        "/api/reservas",
        headers=headers,
        json={
            "data_entrada": entrada.isoformat(),
            "data_saida": saida.isoformat(),
            "quantidade_hospedes": 1,
            "hospede_id": hospede_id,
            "quarto_numero": "301",
            "observacoes": None,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Quartos em manutenção ou inativos não podem ser reservados."

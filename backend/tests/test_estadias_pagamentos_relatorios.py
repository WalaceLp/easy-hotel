from datetime import date, timedelta

from fastapi.testclient import TestClient


def autenticar(client: TestClient, login: str = "admin", senha: str = "admin123") -> dict[str, str]:
    response = client.post("/api/auth/login", json={"login": login, "senha": senha})
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def criar_hospede(client: TestClient, headers: dict[str, str], cpf: str = "39053344705") -> int:
    response = client.post(
        "/api/hospedes",
        headers=headers,
        json={"nome": "João Estadia", "cpf": cpf, "telefone": None, "email": None},
    )
    assert response.status_code == 201
    return int(response.json()["id"])


def criar_reserva_confirmada(client: TestClient, headers: dict[str, str]) -> int:
    hospede_id = criar_hospede(client, headers)
    entrada = date.today() + timedelta(days=2)
    saida = entrada + timedelta(days=2)
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
    confirmacao = client.patch(f"/api/reservas/{reserva_id}/confirmar", headers=headers)
    assert confirmacao.status_code == 200
    return int(reserva_id)


def test_check_in_e_check_out(client: TestClient) -> None:
    headers = autenticar(client)
    reserva_id = criar_reserva_confirmada(client, headers)

    checkin = client.post(
        f"/api/reservas/{reserva_id}/check-in",
        headers=headers,
        json={"observacoes": "Entrada antecipada pelo administrador"},
    )

    assert checkin.status_code == 200
    assert checkin.json()["status"] == "EM_ANDAMENTO"
    assert checkin.json()["quarto"]["status"]["descricao"] == "OCUPADO"

    checkout = client.post(
        f"/api/reservas/{reserva_id}/check-out",
        headers=headers,
        json={"observacoes": "Saída registrada"},
    )

    assert checkout.status_code == 200
    assert checkout.json()["status"] == "CONCLUIDA"
    assert checkout.json()["quarto"]["status"]["descricao"] == "DISPONIVEL"


def test_nao_permite_check_in_duplicado(client: TestClient) -> None:
    headers = autenticar(client)
    reserva_id = criar_reserva_confirmada(client, headers)
    primeiro = client.post(f"/api/reservas/{reserva_id}/check-in", headers=headers, json={})
    assert primeiro.status_code == 200

    segundo = client.post(f"/api/reservas/{reserva_id}/check-in", headers=headers, json={})

    assert segundo.status_code == 409
    assert segundo.json()["detail"] == "Esta reserva já possui check-in registrado."


def test_nao_permite_check_out_sem_check_in(client: TestClient) -> None:
    headers = autenticar(client)
    reserva_id = criar_reserva_confirmada(client, headers)

    response = client.post(f"/api/reservas/{reserva_id}/check-out", headers=headers, json={})

    assert response.status_code == 400
    assert response.json()["detail"] == "Não é permitido check-out sem check-in."


def test_pagamento_nao_ultrapassa_valor_da_reserva(client: TestClient) -> None:
    headers = autenticar(client)
    reserva_id = criar_reserva_confirmada(client, headers)

    pagamento = client.post(
        "/api/pagamentos",
        headers=headers,
        json={"valor": "100.00", "metodo_id": 1, "reserva_id": reserva_id, "observacoes": None},
    )
    assert pagamento.status_code == 201

    excesso = client.post(
        "/api/pagamentos",
        headers=headers,
        json={"valor": "1000.00", "metodo_id": 1, "reserva_id": reserva_id, "observacoes": None},
    )

    assert excesso.status_code == 400
    assert excesso.json()["detail"] == "O total pago não pode ultrapassar o valor da reserva."


def test_saldo_pendente_da_reserva(client: TestClient) -> None:
    headers = autenticar(client)
    reserva_id = criar_reserva_confirmada(client, headers)
    pagamento = client.post(
        "/api/pagamentos",
        headers=headers,
        json={"valor": "100.00", "metodo_id": 1, "reserva_id": reserva_id, "observacoes": None},
    )
    assert pagamento.status_code == 201

    response = client.get(f"/api/reservas/{reserva_id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["total_pago"] == "100.00"
    assert response.json()["saldo_pendente"] == "140.00"


def test_recepcionista_nao_acessa_relatorio_financeiro(client: TestClient) -> None:
    headers = autenticar(client, login="recepcao", senha="recepcao123")

    response = client.get("/api/relatorios/faturamento", headers=headers)

    assert response.status_code == 403


def test_gerente_acessa_relatorio_dashboard(client: TestClient) -> None:
    headers = autenticar(client)

    response = client.get("/api/relatorios/dashboard", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert "total_hospedes" in data
    assert "faturamento_mes" in data

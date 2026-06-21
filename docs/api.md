# API

Base da API:

```text
http://localhost:8000/api
```

## Infraestrutura

```http
GET /health
```

Resposta esperada:

```json
{
  "status": "ok",
  "service": "Easy Hotel"
}
```

## Autenticação

```http
POST /api/auth/login
GET  /api/auth/me
```

Exemplo de login:

```json
{
  "login": "admin",
  "senha": "admin123"
}
```

A resposta retorna um token JWT do tipo Bearer e os dados do usuário autenticado.

Para acessar rotas protegidas:

```http
Authorization: Bearer <token>
```

## Usuários

Rotas restritas ao perfil `ADMINISTRADOR`.

```http
GET   /api/usuarios
POST  /api/usuarios
GET   /api/usuarios/{id}
PUT   /api/usuarios/{id}
PATCH /api/usuarios/{id}/status
```

## Perfis

Rota restrita ao perfil `ADMINISTRADOR`.

```http
GET /api/perfis
```

## Hóspedes

Rotas permitidas para `ADMINISTRADOR`, `GERENTE` e `RECEPCIONISTA`.

```http
GET    /api/hospedes
POST   /api/hospedes
GET    /api/hospedes/{id}
PUT    /api/hospedes/{id}
DELETE /api/hospedes/{id}
```

A exclusão é bloqueada quando há reservas vinculadas ao hóspede.

## Tipos de Quarto

Leitura permitida para usuários autenticados dos três perfis. Escrita restrita a `ADMINISTRADOR` e `GERENTE`.

```http
GET   /api/tipos-quarto
POST  /api/tipos-quarto
GET   /api/tipos-quarto/{id}
PUT   /api/tipos-quarto/{id}
PATCH /api/tipos-quarto/{id}/status
```

## Status de Quarto

```http
GET /api/status-quarto
```

## Quartos

Leitura permitida para usuários autenticados dos três perfis. Escrita restrita a `ADMINISTRADOR` e `GERENTE`.

```http
GET   /api/quartos
POST  /api/quartos
GET   /api/quartos/disponiveis?data_entrada=YYYY-MM-DD&data_saida=YYYY-MM-DD
GET   /api/quartos/{numero}
PUT   /api/quartos/{numero}
PATCH /api/quartos/{numero}/status
```

## Reservas

Rotas permitidas para `ADMINISTRADOR`, `GERENTE` e `RECEPCIONISTA`.

```http
GET   /api/reservas
POST  /api/reservas
GET   /api/reservas/{id}
PUT   /api/reservas/{id}
PATCH /api/reservas/{id}/confirmar
PATCH /api/reservas/{id}/cancelar
POST  /api/reservas/{id}/check-in
POST  /api/reservas/{id}/check-out
```

Regras já aplicadas:

* data de saída posterior à entrada;
* bloqueio de datas passadas;
* bloqueio de conflito de reservas no mesmo quarto;
* reservas canceladas não bloqueiam disponibilidade;
* cálculo automático de `valor_total`.

## Pagamentos

Listagem e consulta geral são restritas a `ADMINISTRADOR` e `GERENTE`. Registro de pagamento e pagamentos por reserva também podem ser acessados por `RECEPCIONISTA`.

```http
GET  /api/pagamentos
POST /api/pagamentos
GET  /api/pagamentos/{id}
GET  /api/reservas/{id}/pagamentos
```

Reservas retornam também `total_pago` e `saldo_pendente`.

## Métodos de Pagamento

Leitura permitida para usuários autenticados dos três perfis. Escrita restrita a `ADMINISTRADOR` e `GERENTE`.

```http
GET   /api/metodos-pagamento
POST  /api/metodos-pagamento
PUT   /api/metodos-pagamento/{id}
PATCH /api/metodos-pagamento/{id}/status
```

## Relatórios

Rotas restritas a `ADMINISTRADOR` e `GERENTE`.

```http
GET /api/relatorios/dashboard
GET /api/relatorios/ocupacao
GET /api/relatorios/faturamento
GET /api/relatorios/reservas
```

Quando aplicável, aceitam filtros `data_inicio=YYYY-MM-DD` e `data_fim=YYYY-MM-DD`.

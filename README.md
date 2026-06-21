# Easy Hotel

Sistema web para auxiliar a gestão de hotéis de pequeno e médio porte, centralizando hóspedes, quartos, reservas, estadias, pagamentos, relatórios e controle de acesso.

## Status

Primeira etapa concluída: estrutura inicial, Docker e banco de dados.

Segunda etapa concluída: backend de autenticação com JWT, usuário autenticado e autorização por perfil.

Terceira etapa concluída: backend de hóspedes, tipos de quarto, quartos e reservas.

Quarta etapa concluída: backend de check-in, check-out, pagamentos e relatórios.

Quinta etapa concluída: frontend funcional, responsivo, com autenticação, rotas protegidas e telas principais.

## Tecnologias

### Frontend

* React
* TypeScript
* Vite
* Tailwind CSS
* React Router
* Axios
* React Hook Form
* Zod

### Backend

* Python
* FastAPI
* SQLAlchemy 2
* Alembic
* Pydantic
* PostgreSQL
* JWT
* Passlib
* Pytest

### Infraestrutura

* Docker
* Docker Compose
* PostgreSQL em container
* Variáveis de ambiente via `.env`

## Execução com Docker

```bash
docker compose up --build
```

Serviços:

* Frontend: `http://localhost:5173`
* Backend: `http://localhost:8000`
* Health check: `http://localhost:8000/health`
* Documentação OpenAPI: `http://localhost:8000/docs`
* PostgreSQL: `localhost:5432`

O backend executa as migrações Alembic e o seed de desenvolvimento antes de iniciar a API.

## Variáveis de ambiente

Arquivos de referência:

* `backend/.env.example`
* `frontend/.env.example`

Para uso local fora do Docker, copie os arquivos para `.env` e ajuste as variáveis conforme o ambiente.

## Credenciais de desenvolvimento

| Perfil | Login | Senha |
| --- | --- | --- |
| `ADMINISTRADOR` | `admin` | `admin123` |
| `GERENTE` | `gerente` | `gerente123` |
| `RECEPCIONISTA` | `recepcao` | `recepcao123` |

Altere essas senhas antes de qualquer uso em produção.

## Estrutura

```text
easy-hotel/
├── backend/
│   ├── alembic/
│   ├── app/
│   ├── tests/
│   ├── alembic.ini
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── .env.example
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   ├── package.json
│   └── .env.example
├── database/
│   └── init.sql
├── docs/
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Banco de dados

A migração inicial cria as tabelas principais:

* perfis
* usuarios
* hospedes
* tipos_quarto
* status_quarto
* quartos
* reservas
* estadias
* metodos_pagamento
* pagamentos

## Migrações

Dentro do container ou ambiente backend:

```bash
alembic upgrade head
```

Seed de desenvolvimento:

```bash
python -m app.database.seed
```

## Testes

Os testes de backend cobrem health check, autenticação, usuário inativo, rota `/me` e autorização por perfil.
Também cobrem CPF inválido/duplicado, cadastro de hóspede, disponibilidade de quartos, cálculo de valor de reserva, conflito de datas, cancelamento e bloqueio de quarto em manutenção.
Também cobrem check-in, check-out, pagamento acima do valor da reserva, saldo pendente e autorização de relatórios.

Comando previsto:

```bash
docker compose exec backend pytest
```

Lint do backend:

```bash
docker compose exec backend ruff check app tests
```

## Endpoints principais

Autenticação:

```http
POST /api/auth/login
GET  /api/auth/me
```

Usuários, restrito a `ADMINISTRADOR`:

```http
GET   /api/usuarios
POST  /api/usuarios
GET   /api/usuarios/{id}
PUT   /api/usuarios/{id}
PATCH /api/usuarios/{id}/status
```

Hóspedes:

```http
GET    /api/hospedes
POST   /api/hospedes
GET    /api/hospedes/{id}
PUT    /api/hospedes/{id}
DELETE /api/hospedes/{id}
```

Quartos e tipos:

```http
GET   /api/tipos-quarto
POST  /api/tipos-quarto
GET   /api/quartos
POST  /api/quartos
GET   /api/quartos/disponiveis
```

Reservas:

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

Pagamentos e relatórios:

```http
GET  /api/pagamentos
POST /api/pagamentos
GET  /api/reservas/{id}/pagamentos
GET  /api/metodos-pagamento
GET  /api/relatorios/dashboard
GET  /api/relatorios/faturamento
```

## Frontend

Páginas implementadas:

* Login
* Dashboard
* Hóspedes
* Cadastro e edição de hóspede
* Quartos
* Tipos de quarto
* Reservas
* Nova reserva
* Detalhes da reserva com check-in, check-out e cancelamento
* Pagamentos
* Usuários
* Relatórios
* Página 404

Componentes reutilizáveis implementados:

* tabela
* busca
* paginação
* modal
* campos de formulário
* confirmação
* alerta
* carregamento
* estado vazio
* badges de status
* cards de métricas

Validação do frontend:

```bash
docker compose exec frontend npm run typecheck
docker compose exec frontend npm run lint
docker compose exec frontend npm run build
```

## Documentação

* `docs/arquitetura.md`
* `docs/banco-de-dados.md`
* `docs/regras-de-negocio.md`
* `docs/api.md`

## Equipe

* Walace Louzada
* Miguel Arcanjo
* Lorenzo Rainha
* Fábio Augusto

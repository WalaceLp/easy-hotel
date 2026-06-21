# Easy Hotel

Sistema web para auxiliar a gestão de hotéis de pequeno e médio porte, centralizando hóspedes, quartos, reservas, estadias, pagamentos, relatórios e controle de acesso.

## Status

Primeira etapa concluída: estrutura inicial, Docker e banco de dados.

As regras de negócio, autenticação completa, endpoints CRUD, frontend funcional e testes serão implementados nas próximas etapas.

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
* PostgreSQL: `localhost:5432`

O backend executa as migrações Alembic e o seed de desenvolvimento antes de iniciar a API.

## Variáveis de ambiente

Arquivos de referência:

* `backend/.env.example`
* `frontend/.env.example`

Para uso local fora do Docker, copie os arquivos para `.env` e ajuste as variáveis conforme o ambiente.

## Credenciais de desenvolvimento

* Login: `admin`
* Senha: `admin123`
* Perfil: `ADMINISTRADOR`

Altere essa senha antes de qualquer uso em produção.

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

A estrutura de testes está preparada em `backend/tests`. A suíte será adicionada junto da implementação das regras de negócio.

Comando previsto:

```bash
pytest
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

# Arquitetura

O Easy Hotel será organizado em frontend React com TypeScript e backend FastAPI com SQLAlchemy.

Nesta primeira etapa foram criadas a estrutura de pastas, a configuração Docker e a base de banco de dados. As regras de negócio, autenticação completa, telas e endpoints CRUD serão implementados nas próximas etapas.

## Backend

* `api`: rotas e dependências HTTP.
* `core`: configurações e segurança.
* `database`: sessão, base declarativa e seed.
* `models`: entidades persistidas.
* `repositories`: acesso ao banco.
* `schemas`: contratos Pydantic.
* `services`: regras de negócio.

## Frontend

* `components`: componentes reutilizáveis.
* `contexts`: estados globais.
* `hooks`: hooks customizados.
* `layouts`: estrutura visual.
* `pages`: páginas.
* `routes`: roteamento e proteção.
* `schemas`: validações.
* `services`: acesso HTTP.
* `types`: tipos TypeScript.
* `utils`: funções auxiliares.

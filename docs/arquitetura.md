# Arquitetura

O Easy Hotel será organizado em frontend React com TypeScript e backend FastAPI com SQLAlchemy.

Na primeira etapa foram criadas a estrutura de pastas, a configuração Docker e a base de banco de dados.

Na segunda etapa foi implementada a autenticação do backend com JWT, proteção de rotas e autorização por perfil. Os demais módulos de negócio serão implementados nas próximas etapas.

## Backend

* `api`: rotas e dependências HTTP.
* `core`: configurações e segurança.
* `database`: sessão, base declarativa e seed.
* `models`: entidades persistidas.
* `repositories`: acesso ao banco.
* `schemas`: contratos Pydantic.
* `services`: regras de negócio.

As rotas HTTP chamam services e repositories; regras como validação de login, usuário inativo, hash de senha e autorização ficam fora das rotas.

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

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

Os demais módulos serão adicionados nas próximas etapas.

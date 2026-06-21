# Banco de Dados

O banco principal é PostgreSQL.

## Entidades criadas

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

## Dados iniciais

A migração inicial cria perfis, status de quarto, métodos de pagamento e tipos de quarto básicos. O seed de desenvolvimento cria também o usuário administrador e quartos de exemplo.

Credenciais de desenvolvimento:

| Perfil | Login | Senha |
| --- | --- | --- |
| `ADMINISTRADOR` | `admin` | `admin123` |
| `GERENTE` | `gerente` | `gerente123` |
| `RECEPCIONISTA` | `recepcao` | `recepcao123` |

Essas senhas devem ser alteradas antes de qualquer uso em produção.

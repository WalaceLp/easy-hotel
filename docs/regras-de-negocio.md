# Regras de Negócio

As regras completas dos módulos de hotelaria serão implementadas nas camadas de serviço nas próximas etapas.

Esta etapa estabeleceu o schema necessário para suportar:

* autenticação e perfis;
* hóspedes;
* quartos e tipos de quarto;
* reservas;
* estadias;
* pagamentos;
* relatórios administrativos.

## Autenticação e autorização

Regras implementadas:

* login por usuário e senha;
* senha armazenada apenas como hash;
* emissão de token JWT;
* consulta do usuário autenticado;
* usuário inativo não pode realizar login;
* rotas administrativas de usuários e perfis restritas ao perfil `ADMINISTRADOR`;
* mensagens claras para token ausente, token inválido, login inválido e permissão insuficiente.

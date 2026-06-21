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

## Hóspedes

Regras implementadas:

* CPF é normalizado para apenas números;
* CPF inválido é recusado;
* CPF duplicado é recusado;
* exclusão é impedida quando houver reservas vinculadas.

## Quartos

Regras implementadas:

* tipos de quarto possuem preço base, capacidade e status ativo;
* quartos possuem tipo, status e controle ativo;
* quartos disponíveis podem ser consultados por período;
* quartos em manutenção ou inativos não podem receber reservas.

## Reservas

Regras implementadas:

* data de saída deve ser posterior à data de entrada;
* data de entrada no passado é recusada;
* o quarto deve existir e estar ativo para receber reservas;
* o tipo do quarto deve estar ativo;
* conflito de reservas para o mesmo quarto e período é recusado;
* reservas canceladas não bloqueiam disponibilidade;
* valor total é calculado por `quantidade de diárias x preço-base do tipo do quarto`;
* reservas pendentes podem ser confirmadas;
* reservas pendentes, confirmadas ou em andamento podem ser canceladas.

## Check-in e Check-out

Regras implementadas:

* check-in exige reserva confirmada;
* check-in antes da data de entrada só é permitido para `ADMINISTRADOR`;
* não é permitido registrar dois check-ins para a mesma reserva;
* ao realizar check-in, a estadia é criada, a reserva muda para `EM_ANDAMENTO` e o quarto muda para `OCUPADO`;
* check-out exige check-in prévio;
* não é permitido registrar dois check-outs para a mesma reserva;
* ao realizar check-out, a estadia recebe a data de saída, a reserva muda para `CONCLUIDA` e o quarto muda para `DISPONIVEL`.

## Pagamentos

Regras implementadas:

* método de pagamento deve existir e estar ativo;
* valor do pagamento deve ser positivo;
* total pago não pode ultrapassar o valor total da reserva;
* reservas informam `total_pago` e `saldo_pendente`.

## Relatórios

Regras implementadas:

* relatórios são restritos a `ADMINISTRADOR` e `GERENTE`;
* dashboard apresenta métricas administrativas, faturamento do mês, taxa de ocupação e reservas recentes;
* relatórios de ocupação, faturamento e reservas aceitam filtros por data quando aplicável.

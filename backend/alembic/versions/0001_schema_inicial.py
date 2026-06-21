"""schema inicial

Revision ID: 0001_schema_inicial
Revises:
Create Date: 2026-06-21 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001_schema_inicial"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "perfis",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nome", sa.String(length=50), nullable=False, unique=True),
    )
    op.create_table(
        "status_quarto",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("descricao", sa.String(length=50), nullable=False, unique=True),
    )
    op.create_table(
        "metodos_pagamento",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("descricao", sa.String(length=50), nullable=False, unique=True),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_table(
        "tipos_quarto",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("descricao", sa.String(length=100), nullable=False, unique=True),
        sa.Column("preco_base", sa.Numeric(10, 2), nullable=False),
        sa.Column("capacidade", sa.Integer(), nullable=False),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column("login", sa.String(length=80), nullable=False, unique=True),
        sa.Column("senha_hash", sa.String(length=255), nullable=False),
        sa.Column("perfil_id", sa.Integer(), sa.ForeignKey("perfis.id"), nullable=False),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("atualizado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table(
        "hospedes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column("cpf", sa.String(length=11), nullable=False, unique=True),
        sa.Column("telefone", sa.String(length=30), nullable=True),
        sa.Column("email", sa.String(length=120), nullable=True),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("atualizado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table(
        "quartos",
        sa.Column("numero", sa.String(length=20), primary_key=True),
        sa.Column("tipo_id", sa.Integer(), sa.ForeignKey("tipos_quarto.id"), nullable=False),
        sa.Column("status_id", sa.Integer(), sa.ForeignKey("status_quarto.id"), nullable=False),
        sa.Column("observacoes", sa.Text(), nullable=True),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("atualizado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table(
        "reservas",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("data_reserva", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("data_entrada", sa.Date(), nullable=False),
        sa.Column("data_saida", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="PENDENTE"),
        sa.Column("quantidade_hospedes", sa.Integer(), nullable=False),
        sa.Column("valor_total", sa.Numeric(10, 2), nullable=False),
        sa.Column("hospede_id", sa.Integer(), sa.ForeignKey("hospedes.id"), nullable=False),
        sa.Column("quarto_numero", sa.String(length=20), sa.ForeignKey("quartos.numero"), nullable=False),
        sa.Column("usuario_id", sa.Integer(), sa.ForeignKey("usuarios.id"), nullable=False),
        sa.Column("observacoes", sa.Text(), nullable=True),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("atualizado_em", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table(
        "estadias",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("reserva_id", sa.Integer(), sa.ForeignKey("reservas.id"), nullable=False, unique=True),
        sa.Column("data_checkin", sa.DateTime(timezone=True), nullable=False),
        sa.Column("data_checkout", sa.DateTime(timezone=True), nullable=True),
        sa.Column("usuario_checkin_id", sa.Integer(), sa.ForeignKey("usuarios.id"), nullable=False),
        sa.Column("usuario_checkout_id", sa.Integer(), sa.ForeignKey("usuarios.id"), nullable=True),
        sa.Column("observacoes", sa.Text(), nullable=True),
    )
    op.create_table(
        "pagamentos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("valor", sa.Numeric(10, 2), nullable=False),
        sa.Column("data_pagamento", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("metodo_id", sa.Integer(), sa.ForeignKey("metodos_pagamento.id"), nullable=False),
        sa.Column("reserva_id", sa.Integer(), sa.ForeignKey("reservas.id"), nullable=False),
        sa.Column("usuario_id", sa.Integer(), sa.ForeignKey("usuarios.id"), nullable=False),
        sa.Column("observacoes", sa.Text(), nullable=True),
    )

    op.bulk_insert(sa.table("perfis", sa.column("nome")), [
        {"nome": "ADMINISTRADOR"},
        {"nome": "GERENTE"},
        {"nome": "RECEPCIONISTA"},
    ])
    op.bulk_insert(sa.table("status_quarto", sa.column("descricao")), [
        {"descricao": "DISPONIVEL"},
        {"descricao": "RESERVADO"},
        {"descricao": "OCUPADO"},
        {"descricao": "MANUTENCAO"},
        {"descricao": "INATIVO"},
    ])
    op.bulk_insert(sa.table("metodos_pagamento", sa.column("descricao")), [
        {"descricao": "DINHEIRO"},
        {"descricao": "PIX"},
        {"descricao": "CARTAO_CREDITO"},
        {"descricao": "CARTAO_DEBITO"},
    ])
    op.bulk_insert(sa.table("tipos_quarto", sa.column("descricao"), sa.column("preco_base"), sa.column("capacidade")), [
        {"descricao": "Solteiro", "preco_base": 120.00, "capacidade": 1},
        {"descricao": "Casal", "preco_base": 180.00, "capacidade": 2},
        {"descricao": "Familia", "preco_base": 260.00, "capacidade": 4},
    ])


def downgrade() -> None:
    op.drop_table("pagamentos")
    op.drop_table("estadias")
    op.drop_table("reservas")
    op.drop_table("quartos")
    op.drop_table("hospedes")
    op.drop_table("usuarios")
    op.drop_table("tipos_quarto")
    op.drop_table("metodos_pagamento")
    op.drop_table("status_quarto")
    op.drop_table("perfis")

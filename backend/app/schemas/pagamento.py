from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class MetodoPagamentoBase(BaseModel):
    descricao: str = Field(min_length=2, max_length=50)
    ativo: bool = True


class MetodoPagamentoCreate(MetodoPagamentoBase):
    pass


class MetodoPagamentoUpdate(MetodoPagamentoBase):
    pass


class MetodoPagamentoStatusUpdate(BaseModel):
    ativo: bool


class MetodoPagamentoRead(BaseModel):
    id: int
    descricao: str
    ativo: bool

    model_config = ConfigDict(from_attributes=True)


class PagamentoCreate(BaseModel):
    valor: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    metodo_id: int
    reserva_id: int
    observacoes: str | None = None


class PagamentoRead(BaseModel):
    id: int
    valor: Decimal
    data_pagamento: datetime
    metodo_id: int
    reserva_id: int
    usuario_id: int
    observacoes: str | None
    metodo: MetodoPagamentoRead

    model_config = ConfigDict(from_attributes=True)

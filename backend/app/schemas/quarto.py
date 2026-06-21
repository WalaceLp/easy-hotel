from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class TipoQuartoBase(BaseModel):
    descricao: str = Field(min_length=2, max_length=100)
    preco_base: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    capacidade: int = Field(gt=0)
    ativo: bool = True


class TipoQuartoCreate(TipoQuartoBase):
    pass


class TipoQuartoUpdate(TipoQuartoBase):
    pass


class TipoQuartoStatusUpdate(BaseModel):
    ativo: bool


class TipoQuartoRead(BaseModel):
    id: int
    descricao: str
    preco_base: Decimal
    capacidade: int
    ativo: bool

    model_config = ConfigDict(from_attributes=True)


class StatusQuartoRead(BaseModel):
    id: int
    descricao: str

    model_config = ConfigDict(from_attributes=True)


class QuartoBase(BaseModel):
    numero: str = Field(min_length=1, max_length=20)
    tipo_id: int
    status_id: int
    observacoes: str | None = None
    ativo: bool = True


class QuartoCreate(QuartoBase):
    pass


class QuartoUpdate(BaseModel):
    tipo_id: int
    status_id: int
    observacoes: str | None = None
    ativo: bool = True


class QuartoStatusUpdate(BaseModel):
    status_id: int
    ativo: bool | None = None


class QuartoRead(BaseModel):
    numero: str
    tipo_id: int
    status_id: int
    observacoes: str | None
    ativo: bool
    criado_em: datetime
    atualizado_em: datetime
    tipo: TipoQuartoRead
    status: StatusQuartoRead

    model_config = ConfigDict(from_attributes=True)

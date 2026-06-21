from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.hospede import HospedeRead
from app.schemas.quarto import QuartoRead
from app.schemas.usuario import UsuarioRead


class ReservaBase(BaseModel):
    data_entrada: date
    data_saida: date
    quantidade_hospedes: int = Field(gt=0)
    hospede_id: int
    quarto_numero: str = Field(min_length=1, max_length=20)
    observacoes: str | None = None

    @model_validator(mode="after")
    def validar_periodo(self) -> "ReservaBase":
        if self.data_saida <= self.data_entrada:
            raise ValueError("A data de saída deve ser posterior à data de entrada.")
        return self


class ReservaCreate(ReservaBase):
    pass


class ReservaUpdate(ReservaBase):
    pass


class ReservaRead(BaseModel):
    id: int
    data_reserva: datetime
    data_entrada: date
    data_saida: date
    status: str
    quantidade_hospedes: int
    valor_total: Decimal
    total_pago: Decimal
    saldo_pendente: Decimal
    hospede_id: int
    quarto_numero: str
    usuario_id: int
    observacoes: str | None
    criado_em: datetime
    atualizado_em: datetime
    hospede: HospedeRead
    quarto: QuartoRead
    usuario: UsuarioRead

    model_config = ConfigDict(from_attributes=True)

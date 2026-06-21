from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CheckInRequest(BaseModel):
    observacoes: str | None = None


class CheckOutRequest(BaseModel):
    observacoes: str | None = None


class EstadiaRead(BaseModel):
    id: int
    reserva_id: int
    data_checkin: datetime
    data_checkout: datetime | None
    usuario_checkin_id: int
    usuario_checkout_id: int | None
    observacoes: str | None

    model_config = ConfigDict(from_attributes=True)

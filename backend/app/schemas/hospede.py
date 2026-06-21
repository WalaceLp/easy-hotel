from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class HospedeBase(BaseModel):
    nome: str = Field(min_length=2, max_length=120)
    cpf: str = Field(min_length=11, max_length=14)
    telefone: str | None = Field(default=None, max_length=30)
    email: EmailStr | None = None


class HospedeCreate(HospedeBase):
    pass


class HospedeUpdate(HospedeBase):
    pass


class HospedeRead(BaseModel):
    id: int
    nome: str
    cpf: str
    telefone: str | None
    email: str | None
    criado_em: datetime
    atualizado_em: datetime

    model_config = ConfigDict(from_attributes=True)

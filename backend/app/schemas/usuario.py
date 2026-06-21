from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.perfil import PerfilRead


class UsuarioBase(BaseModel):
    nome: str = Field(min_length=2, max_length=120)
    login: str = Field(min_length=3, max_length=80)
    perfil_id: int
    ativo: bool = True


class UsuarioCreate(UsuarioBase):
    senha: str = Field(min_length=6, max_length=72)


class UsuarioUpdate(BaseModel):
    nome: str = Field(min_length=2, max_length=120)
    login: str = Field(min_length=3, max_length=80)
    perfil_id: int
    ativo: bool = True
    senha: str | None = Field(default=None, min_length=6, max_length=72)


class UsuarioStatusUpdate(BaseModel):
    ativo: bool


class UsuarioRead(BaseModel):
    id: int
    nome: str
    login: str
    perfil_id: int
    ativo: bool
    criado_em: datetime
    atualizado_em: datetime
    perfil: PerfilRead

    model_config = ConfigDict(from_attributes=True)

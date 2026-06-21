from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.dependencies import exigir_perfis
from app.database.session import get_db
from app.models import Usuario
from app.schemas import HospedeCreate, HospedeRead, HospedeUpdate
from app.services import HospedeService

router = APIRouter(prefix="/hospedes", tags=["hóspedes"])

OperadorHospedes = Annotated[
    Usuario,
    Depends(exigir_perfis("ADMINISTRADOR", "GERENTE", "RECEPCIONISTA")),
]


@router.get("", response_model=list[HospedeRead])
def listar_hospedes(
    db: Annotated[Session, Depends(get_db)],
    _: OperadorHospedes,
) -> list:
    return HospedeService(db).listar()


@router.post("", response_model=HospedeRead, status_code=status.HTTP_201_CREATED)
def criar_hospede(
    dados: HospedeCreate,
    db: Annotated[Session, Depends(get_db)],
    _: OperadorHospedes,
):
    return HospedeService(db).criar(dados)


@router.get("/{hospede_id}", response_model=HospedeRead)
def buscar_hospede(
    hospede_id: int,
    db: Annotated[Session, Depends(get_db)],
    _: OperadorHospedes,
):
    return HospedeService(db).buscar_por_id(hospede_id)


@router.put("/{hospede_id}", response_model=HospedeRead)
def atualizar_hospede(
    hospede_id: int,
    dados: HospedeUpdate,
    db: Annotated[Session, Depends(get_db)],
    _: OperadorHospedes,
):
    return HospedeService(db).atualizar(hospede_id, dados)


@router.delete("/{hospede_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_hospede(
    hospede_id: int,
    db: Annotated[Session, Depends(get_db)],
    _: OperadorHospedes,
) -> Response:
    HospedeService(db).excluir(hospede_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

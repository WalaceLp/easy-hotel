from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import exigir_perfis
from app.database.session import get_db
from app.models import Usuario
from app.repositories import PerfilRepository
from app.schemas import PerfilRead

router = APIRouter(prefix="/perfis", tags=["perfis"])


@router.get("", response_model=list[PerfilRead])
def listar_perfis(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[Usuario, Depends(exigir_perfis("ADMINISTRADOR"))],
) -> list:
    return PerfilRepository(db).listar()

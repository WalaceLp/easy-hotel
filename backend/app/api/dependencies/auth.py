from collections.abc import Callable
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decodificar_token
from app.database.session import get_db
from app.models import Usuario
from app.repositories import UsuarioRepository

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> Usuario:
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação não informado.",
        )

    try:
        payload = decodificar_token(credentials.credentials)
        usuario_id = int(payload["sub"])
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado.",
        ) from exc

    usuario = UsuarioRepository(db).buscar_por_id(usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário autenticado não encontrado.",
        )

    if not usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo não pode acessar o sistema.",
        )

    return usuario


def exigir_perfis(*perfis_permitidos: str) -> Callable[[Usuario], Usuario]:
    def dependency(usuario: Annotated[Usuario, Depends(get_current_user)]) -> Usuario:
        perfil = usuario.perfil.nome
        if perfil not in perfis_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuário não possui permissão para acessar este recurso.",
            )
        return usuario

    return dependency


UsuarioAtual = Annotated[Usuario, Depends(get_current_user)]

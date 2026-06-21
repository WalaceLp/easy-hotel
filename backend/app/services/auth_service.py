from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import criar_token_acesso, verificar_senha
from app.models import Usuario
from app.repositories import UsuarioRepository


class AuthService:
    def __init__(self, db: Session) -> None:
        self.usuario_repository = UsuarioRepository(db)

    def autenticar(self, login: str, senha: str) -> tuple[str, Usuario]:
        usuario = self.usuario_repository.buscar_por_login(login)
        if not usuario or not verificar_senha(senha, usuario.senha_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Login ou senha inválidos.",
            )

        if not usuario.ativo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuário inativo não pode realizar login.",
            )

        token = criar_token_acesso(str(usuario.id))
        return token, usuario

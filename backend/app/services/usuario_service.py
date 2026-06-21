from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import gerar_hash_senha
from app.models import Usuario
from app.repositories import PerfilRepository, UsuarioRepository
from app.schemas import UsuarioCreate, UsuarioStatusUpdate, UsuarioUpdate


class UsuarioService:
    def __init__(self, db: Session) -> None:
        self.usuario_repository = UsuarioRepository(db)
        self.perfil_repository = PerfilRepository(db)

    def listar(self) -> list[Usuario]:
        return self.usuario_repository.listar()

    def buscar_por_id(self, usuario_id: int) -> Usuario:
        usuario = self.usuario_repository.buscar_por_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado.",
            )
        return usuario

    def criar(self, dados: UsuarioCreate) -> Usuario:
        self._validar_perfil(dados.perfil_id)
        self._validar_login_disponivel(dados.login)

        usuario = Usuario(
            nome=dados.nome,
            login=dados.login,
            senha_hash=gerar_hash_senha(dados.senha),
            perfil_id=dados.perfil_id,
            ativo=dados.ativo,
        )
        usuario = self.usuario_repository.adicionar(usuario)
        self.usuario_repository.salvar()
        return usuario

    def atualizar(self, usuario_id: int, dados: UsuarioUpdate) -> Usuario:
        usuario = self.buscar_por_id(usuario_id)
        self._validar_perfil(dados.perfil_id)
        self._validar_login_disponivel(dados.login, ignorar_usuario_id=usuario_id)

        usuario.nome = dados.nome
        usuario.login = dados.login
        usuario.perfil_id = dados.perfil_id
        usuario.ativo = dados.ativo
        if dados.senha:
            usuario.senha_hash = gerar_hash_senha(dados.senha)

        self.usuario_repository.salvar()
        return self.buscar_por_id(usuario_id)

    def atualizar_status(self, usuario_id: int, dados: UsuarioStatusUpdate) -> Usuario:
        usuario = self.buscar_por_id(usuario_id)
        usuario.ativo = dados.ativo
        self.usuario_repository.salvar()
        return self.buscar_por_id(usuario_id)

    def _validar_perfil(self, perfil_id: int) -> None:
        if not self.perfil_repository.buscar_por_id(perfil_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Perfil informado não existe.",
            )

    def _validar_login_disponivel(
        self, login: str, ignorar_usuario_id: int | None = None
    ) -> None:
        if self.usuario_repository.existe_login(login, ignorar_usuario_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe usuário cadastrado com este login.",
            )

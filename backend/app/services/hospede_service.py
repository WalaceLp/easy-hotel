from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.validators import cpf_valido, limpar_cpf
from app.models import Hospede
from app.repositories import HospedeRepository
from app.schemas import HospedeCreate, HospedeUpdate


class HospedeService:
    def __init__(self, db: Session) -> None:
        self.hospede_repository = HospedeRepository(db)

    def listar(self) -> list[Hospede]:
        return self.hospede_repository.listar()

    def buscar_por_id(self, hospede_id: int) -> Hospede:
        hospede = self.hospede_repository.buscar_por_id(hospede_id)
        if not hospede:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hóspede não encontrado.")
        return hospede

    def criar(self, dados: HospedeCreate) -> Hospede:
        cpf = self._validar_cpf(dados.cpf)
        self._validar_cpf_disponivel(cpf)

        hospede = Hospede(
            nome=dados.nome,
            cpf=cpf,
            telefone=dados.telefone,
            email=str(dados.email) if dados.email else None,
        )
        hospede = self.hospede_repository.adicionar(hospede)
        self.hospede_repository.salvar()
        return hospede

    def atualizar(self, hospede_id: int, dados: HospedeUpdate) -> Hospede:
        hospede = self.buscar_por_id(hospede_id)
        cpf = self._validar_cpf(dados.cpf)
        self._validar_cpf_disponivel(cpf, ignorar_hospede_id=hospede_id)

        hospede.nome = dados.nome
        hospede.cpf = cpf
        hospede.telefone = dados.telefone
        hospede.email = str(dados.email) if dados.email else None
        self.hospede_repository.salvar()
        return self.buscar_por_id(hospede_id)

    def excluir(self, hospede_id: int) -> None:
        hospede = self.buscar_por_id(hospede_id)
        if self.hospede_repository.possui_reservas(hospede_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Não é possível excluir hóspede com reservas vinculadas.",
            )
        self.hospede_repository.excluir(hospede)
        self.hospede_repository.salvar()

    def _validar_cpf(self, cpf: str) -> str:
        cpf_limpo = limpar_cpf(cpf)
        if not cpf_valido(cpf_limpo):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CPF inválido.")
        return cpf_limpo

    def _validar_cpf_disponivel(self, cpf: str, ignorar_hospede_id: int | None = None) -> None:
        if self.hospede_repository.existe_cpf(cpf, ignorar_hospede_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe hóspede cadastrado com este CPF.",
            )

from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Quarto, StatusQuarto, TipoQuarto
from app.repositories import QuartoRepository, StatusQuartoRepository, TipoQuartoRepository
from app.schemas import (
    QuartoCreate,
    QuartoStatusUpdate,
    QuartoUpdate,
    TipoQuartoCreate,
    TipoQuartoStatusUpdate,
    TipoQuartoUpdate,
)


class TipoQuartoService:
    def __init__(self, db: Session) -> None:
        self.tipo_repository = TipoQuartoRepository(db)

    def listar(self) -> list[TipoQuarto]:
        return self.tipo_repository.listar()

    def buscar_por_id(self, tipo_id: int) -> TipoQuarto:
        tipo = self.tipo_repository.buscar_por_id(tipo_id)
        if not tipo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de quarto não encontrado.")
        return tipo

    def criar(self, dados: TipoQuartoCreate) -> TipoQuarto:
        self._validar_descricao_disponivel(dados.descricao)
        tipo = TipoQuarto(
            descricao=dados.descricao,
            preco_base=dados.preco_base,
            capacidade=dados.capacidade,
            ativo=dados.ativo,
        )
        tipo = self.tipo_repository.adicionar(tipo)
        self.tipo_repository.salvar()
        return tipo

    def atualizar(self, tipo_id: int, dados: TipoQuartoUpdate) -> TipoQuarto:
        tipo = self.buscar_por_id(tipo_id)
        self._validar_descricao_disponivel(dados.descricao, ignorar_tipo_id=tipo_id)
        tipo.descricao = dados.descricao
        tipo.preco_base = dados.preco_base
        tipo.capacidade = dados.capacidade
        tipo.ativo = dados.ativo
        self.tipo_repository.salvar()
        return self.buscar_por_id(tipo_id)

    def atualizar_status(self, tipo_id: int, dados: TipoQuartoStatusUpdate) -> TipoQuarto:
        tipo = self.buscar_por_id(tipo_id)
        tipo.ativo = dados.ativo
        self.tipo_repository.salvar()
        return self.buscar_por_id(tipo_id)

    def _validar_descricao_disponivel(self, descricao: str, ignorar_tipo_id: int | None = None) -> None:
        if self.tipo_repository.existe_descricao(descricao, ignorar_tipo_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe tipo de quarto cadastrado com esta descrição.",
            )


class QuartoService:
    def __init__(self, db: Session) -> None:
        self.quarto_repository = QuartoRepository(db)
        self.tipo_repository = TipoQuartoRepository(db)
        self.status_repository = StatusQuartoRepository(db)

    def listar(self) -> list[Quarto]:
        return self.quarto_repository.listar()

    def listar_status(self) -> list[StatusQuarto]:
        return self.status_repository.listar()

    def buscar_por_numero(self, numero: str) -> Quarto:
        quarto = self.quarto_repository.buscar_por_numero(numero)
        if not quarto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quarto não encontrado.")
        return quarto

    def criar(self, dados: QuartoCreate) -> Quarto:
        if self.quarto_repository.existe_numero(dados.numero):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe quarto cadastrado com este número.",
            )
        self._validar_tipo(dados.tipo_id)
        self._validar_status(dados.status_id)
        quarto = Quarto(
            numero=dados.numero,
            tipo_id=dados.tipo_id,
            status_id=dados.status_id,
            observacoes=dados.observacoes,
            ativo=dados.ativo,
        )
        quarto = self.quarto_repository.adicionar(quarto)
        self.quarto_repository.salvar()
        return quarto

    def atualizar(self, numero: str, dados: QuartoUpdate) -> Quarto:
        quarto = self.buscar_por_numero(numero)
        self._validar_tipo(dados.tipo_id)
        self._validar_status(dados.status_id)
        quarto.tipo_id = dados.tipo_id
        quarto.status_id = dados.status_id
        quarto.observacoes = dados.observacoes
        quarto.ativo = dados.ativo
        self.quarto_repository.salvar()
        return self.buscar_por_numero(numero)

    def atualizar_status(self, numero: str, dados: QuartoStatusUpdate) -> Quarto:
        quarto = self.buscar_por_numero(numero)
        self._validar_status(dados.status_id)
        quarto.status_id = dados.status_id
        if dados.ativo is not None:
            quarto.ativo = dados.ativo
        self.quarto_repository.salvar()
        return self.buscar_por_numero(numero)

    def listar_disponiveis(self, data_entrada: date, data_saida: date) -> list[Quarto]:
        self._validar_periodo(data_entrada, data_saida)
        return self.quarto_repository.listar_disponiveis(data_entrada, data_saida)

    def _validar_tipo(self, tipo_id: int) -> None:
        if not self.tipo_repository.buscar_por_id(tipo_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de quarto não encontrado.")

    def _validar_status(self, status_id: int) -> None:
        if not self.status_repository.buscar_por_id(status_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Status do quarto não encontrado.")

    def _validar_periodo(self, data_entrada: date, data_saida: date) -> None:
        if data_saida <= data_entrada:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A data de saída deve ser posterior à data de entrada.",
            )

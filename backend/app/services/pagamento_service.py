from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import MetodoPagamento, Pagamento, Usuario
from app.repositories import MetodoPagamentoRepository, PagamentoRepository, ReservaRepository
from app.schemas import (
    MetodoPagamentoCreate,
    MetodoPagamentoStatusUpdate,
    MetodoPagamentoUpdate,
    PagamentoCreate,
)


class MetodoPagamentoService:
    def __init__(self, db: Session) -> None:
        self.metodo_repository = MetodoPagamentoRepository(db)

    def listar(self) -> list[MetodoPagamento]:
        return self.metodo_repository.listar()

    def buscar_por_id(self, metodo_id: int) -> MetodoPagamento:
        metodo = self.metodo_repository.buscar_por_id(metodo_id)
        if not metodo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Método de pagamento não encontrado.",
            )
        return metodo

    def criar(self, dados: MetodoPagamentoCreate) -> MetodoPagamento:
        self._validar_descricao_disponivel(dados.descricao)
        metodo = MetodoPagamento(descricao=dados.descricao, ativo=dados.ativo)
        metodo = self.metodo_repository.adicionar(metodo)
        self.metodo_repository.salvar()
        return metodo

    def atualizar(self, metodo_id: int, dados: MetodoPagamentoUpdate) -> MetodoPagamento:
        metodo = self.buscar_por_id(metodo_id)
        self._validar_descricao_disponivel(dados.descricao, metodo_id)
        metodo.descricao = dados.descricao
        metodo.ativo = dados.ativo
        self.metodo_repository.salvar()
        return self.buscar_por_id(metodo_id)

    def atualizar_status(self, metodo_id: int, dados: MetodoPagamentoStatusUpdate) -> MetodoPagamento:
        metodo = self.buscar_por_id(metodo_id)
        metodo.ativo = dados.ativo
        self.metodo_repository.salvar()
        return self.buscar_por_id(metodo_id)

    def _validar_descricao_disponivel(
        self, descricao: str, ignorar_metodo_id: int | None = None
    ) -> None:
        if self.metodo_repository.existe_descricao(descricao, ignorar_metodo_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe método de pagamento cadastrado com esta descrição.",
            )


class PagamentoService:
    def __init__(self, db: Session) -> None:
        self.pagamento_repository = PagamentoRepository(db)
        self.metodo_repository = MetodoPagamentoRepository(db)
        self.reserva_repository = ReservaRepository(db)

    def listar(self) -> list[Pagamento]:
        return self.pagamento_repository.listar()

    def buscar_por_id(self, pagamento_id: int) -> Pagamento:
        pagamento = self.pagamento_repository.buscar_por_id(pagamento_id)
        if not pagamento:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pagamento não encontrado.")
        return pagamento

    def listar_por_reserva(self, reserva_id: int) -> list[Pagamento]:
        if not self.reserva_repository.buscar_por_id(reserva_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva não encontrada.")
        return self.pagamento_repository.listar_por_reserva(reserva_id)

    def criar(self, dados: PagamentoCreate, usuario: Usuario) -> Pagamento:
        reserva = self.reserva_repository.buscar_por_id(dados.reserva_id)
        if not reserva:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva não encontrada.")

        metodo = self.metodo_repository.buscar_por_id(dados.metodo_id)
        if not metodo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Método de pagamento não encontrado.",
            )
        if not metodo.ativo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Método de pagamento inativo não pode ser utilizado.",
            )

        total_pago = self.pagamento_repository.total_por_reserva(dados.reserva_id)
        if total_pago + dados.valor > reserva.valor_total:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O total pago não pode ultrapassar o valor da reserva.",
            )

        pagamento = Pagamento(
            valor=dados.valor,
            metodo_id=dados.metodo_id,
            reserva_id=dados.reserva_id,
            usuario_id=usuario.id,
            observacoes=dados.observacoes,
        )
        pagamento = self.pagamento_repository.adicionar(pagamento)
        self.pagamento_repository.salvar()
        return pagamento

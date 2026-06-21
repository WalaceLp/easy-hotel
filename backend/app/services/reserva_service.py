from datetime import date
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Reserva, Usuario
from app.repositories import HospedeRepository, QuartoRepository, ReservaRepository
from app.schemas import ReservaCreate, ReservaUpdate

STATUS_RESERVA = {"PENDENTE", "CONFIRMADA", "EM_ANDAMENTO", "CONCLUIDA", "CANCELADA"}


class ReservaService:
    def __init__(self, db: Session) -> None:
        self.reserva_repository = ReservaRepository(db)
        self.hospede_repository = HospedeRepository(db)
        self.quarto_repository = QuartoRepository(db)

    def listar(self) -> list[Reserva]:
        return self.reserva_repository.listar()

    def buscar_por_id(self, reserva_id: int) -> Reserva:
        reserva = self.reserva_repository.buscar_por_id(reserva_id)
        if not reserva:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva não encontrada.")
        return reserva

    def criar(self, dados: ReservaCreate, usuario: Usuario) -> Reserva:
        self._validar_base(dados)
        quarto = self._validar_quarto_reservavel(dados.quarto_numero)
        self._validar_conflito(dados.quarto_numero, dados.data_entrada, dados.data_saida)

        reserva = Reserva(
            data_entrada=dados.data_entrada,
            data_saida=dados.data_saida,
            status="PENDENTE",
            quantidade_hospedes=dados.quantidade_hospedes,
            valor_total=self._calcular_valor(dados.data_entrada, dados.data_saida, quarto.tipo.preco_base),
            hospede_id=dados.hospede_id,
            quarto_numero=dados.quarto_numero,
            usuario_id=usuario.id,
            observacoes=dados.observacoes,
        )
        reserva = self.reserva_repository.adicionar(reserva)
        self.reserva_repository.salvar()
        return reserva

    def atualizar(self, reserva_id: int, dados: ReservaUpdate) -> Reserva:
        reserva = self.buscar_por_id(reserva_id)
        if reserva.status in {"CONCLUIDA", "CANCELADA"}:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não é possível alterar reserva concluída ou cancelada.",
            )

        self._validar_base(dados)
        quarto = self._validar_quarto_reservavel(dados.quarto_numero)
        self._validar_conflito(dados.quarto_numero, dados.data_entrada, dados.data_saida, reserva_id)

        reserva.data_entrada = dados.data_entrada
        reserva.data_saida = dados.data_saida
        reserva.quantidade_hospedes = dados.quantidade_hospedes
        reserva.valor_total = self._calcular_valor(dados.data_entrada, dados.data_saida, quarto.tipo.preco_base)
        reserva.hospede_id = dados.hospede_id
        reserva.quarto_numero = dados.quarto_numero
        reserva.observacoes = dados.observacoes
        self.reserva_repository.salvar()
        return self.buscar_por_id(reserva_id)

    def confirmar(self, reserva_id: int) -> Reserva:
        reserva = self.buscar_por_id(reserva_id)
        if reserva.status != "PENDENTE":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Apenas reservas pendentes podem ser confirmadas.",
            )
        reserva.status = "CONFIRMADA"
        self.reserva_repository.salvar()
        return self.buscar_por_id(reserva_id)

    def cancelar(self, reserva_id: int) -> Reserva:
        reserva = self.buscar_por_id(reserva_id)
        if reserva.status in {"CONCLUIDA", "CANCELADA"}:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reserva concluída ou já cancelada não pode ser cancelada.",
            )
        reserva.status = "CANCELADA"
        self.reserva_repository.salvar()
        return self.buscar_por_id(reserva_id)

    def _validar_base(self, dados: ReservaCreate | ReservaUpdate) -> None:
        if dados.data_saida <= dados.data_entrada:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A data de saída deve ser posterior à data de entrada.",
            )
        if dados.data_entrada < date.today():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não é permitido criar reserva com data de entrada no passado.",
            )
        if not self.hospede_repository.buscar_por_id(dados.hospede_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Hóspede não encontrado.")

    def _validar_quarto_reservavel(self, numero: str):
        quarto = self.quarto_repository.buscar_por_numero(numero)
        if not quarto:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quarto não encontrado.")
        if not quarto.ativo or not quarto.tipo.ativo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O quarto deve estar ativo para receber reservas.",
            )
        if quarto.status.descricao in {"MANUTENCAO", "INATIVO"}:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quartos em manutenção ou inativos não podem ser reservados.",
            )
        return quarto

    def _validar_conflito(
        self,
        quarto_numero: str,
        data_entrada: date,
        data_saida: date,
        ignorar_reserva_id: int | None = None,
    ) -> None:
        if self.reserva_repository.existe_conflito(
            quarto_numero, data_entrada, data_saida, ignorar_reserva_id
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe reserva para este quarto no período informado.",
            )

    def _calcular_valor(self, data_entrada: date, data_saida: date, preco_base: Decimal) -> Decimal:
        diarias = (data_saida - data_entrada).days
        return Decimal(diarias) * preco_base

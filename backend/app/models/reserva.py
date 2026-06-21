from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import TimestampMixin


class Reserva(TimestampMixin, Base):
    __tablename__ = "reservas"

    id: Mapped[int] = mapped_column(primary_key=True)
    data_reserva: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    data_entrada: Mapped[date] = mapped_column(Date, nullable=False)
    data_saida: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="PENDENTE", nullable=False)
    quantidade_hospedes: Mapped[int] = mapped_column(nullable=False)
    valor_total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    hospede_id: Mapped[int] = mapped_column(ForeignKey("hospedes.id"), nullable=False)
    quarto_numero: Mapped[str] = mapped_column(ForeignKey("quartos.numero"), nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    observacoes: Mapped[str | None] = mapped_column(Text)

    hospede = relationship("Hospede", back_populates="reservas")
    quarto = relationship("Quarto", back_populates="reservas")
    usuario = relationship("Usuario", back_populates="reservas")
    estadia = relationship("Estadia", back_populates="reserva", uselist=False)
    pagamentos = relationship("Pagamento", back_populates="reserva")

    @property
    def total_pago(self) -> Decimal:
        return sum((pagamento.valor for pagamento in self.pagamentos), Decimal("0.00"))

    @property
    def saldo_pendente(self) -> Decimal:
        return self.valor_total - self.total_pago

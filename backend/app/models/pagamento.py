from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Pagamento(Base):
    __tablename__ = "pagamentos"

    id: Mapped[int] = mapped_column(primary_key=True)
    valor: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    data_pagamento: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    metodo_id: Mapped[int] = mapped_column(ForeignKey("metodos_pagamento.id"), nullable=False)
    reserva_id: Mapped[int] = mapped_column(ForeignKey("reservas.id"), nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    observacoes: Mapped[str | None] = mapped_column(Text)

    metodo = relationship("MetodoPagamento", back_populates="pagamentos")
    reserva = relationship("Reserva", back_populates="pagamentos")

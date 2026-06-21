from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import TimestampMixin


class Quarto(TimestampMixin, Base):
    __tablename__ = "quartos"

    numero: Mapped[str] = mapped_column(String(20), primary_key=True)
    tipo_id: Mapped[int] = mapped_column(ForeignKey("tipos_quarto.id"), nullable=False)
    status_id: Mapped[int] = mapped_column(ForeignKey("status_quarto.id"), nullable=False)
    observacoes: Mapped[str | None] = mapped_column(Text)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    tipo = relationship("TipoQuarto", back_populates="quartos")
    status = relationship("StatusQuarto", back_populates="quartos")
    reservas = relationship("Reserva", back_populates="quarto")

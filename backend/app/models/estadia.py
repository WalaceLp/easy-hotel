from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Estadia(Base):
    __tablename__ = "estadias"

    id: Mapped[int] = mapped_column(primary_key=True)
    reserva_id: Mapped[int] = mapped_column(ForeignKey("reservas.id"), unique=True, nullable=False)
    data_checkin: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    data_checkout: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    usuario_checkin_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    usuario_checkout_id: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id"))
    observacoes: Mapped[str | None] = mapped_column(Text)

    reserva = relationship("Reserva", back_populates="estadia")

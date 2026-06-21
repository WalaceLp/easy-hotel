from decimal import Decimal

from sqlalchemy import Boolean, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class TipoQuarto(Base):
    __tablename__ = "tipos_quarto"

    id: Mapped[int] = mapped_column(primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    preco_base: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    capacidade: Mapped[int] = mapped_column(nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    quartos = relationship("Quarto", back_populates="tipo")

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class StatusQuarto(Base):
    __tablename__ = "status_quarto"

    id: Mapped[int] = mapped_column(primary_key=True)
    descricao: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    quartos = relationship("Quarto", back_populates="status")

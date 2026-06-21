from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import Quarto, Reserva, StatusQuarto, TipoQuarto

STATUS_RESERVAS_BLOQUEANTES = ("PENDENTE", "CONFIRMADA", "EM_ANDAMENTO")


class TipoQuartoRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def listar(self) -> list[TipoQuarto]:
        return list(self.db.scalars(select(TipoQuarto).order_by(TipoQuarto.descricao)).all())

    def buscar_por_id(self, tipo_id: int) -> TipoQuarto | None:
        return self.db.get(TipoQuarto, tipo_id)

    def existe_descricao(self, descricao: str, ignorar_tipo_id: int | None = None) -> bool:
        stmt = select(TipoQuarto.id).where(TipoQuarto.descricao == descricao)
        if ignorar_tipo_id is not None:
            stmt = stmt.where(TipoQuarto.id != ignorar_tipo_id)
        return self.db.scalar(stmt) is not None

    def adicionar(self, tipo: TipoQuarto) -> TipoQuarto:
        self.db.add(tipo)
        self.db.flush()
        self.db.refresh(tipo)
        return tipo

    def salvar(self) -> None:
        self.db.commit()


class StatusQuartoRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def listar(self) -> list[StatusQuarto]:
        return list(self.db.scalars(select(StatusQuarto).order_by(StatusQuarto.id)).all())

    def buscar_por_id(self, status_id: int) -> StatusQuarto | None:
        return self.db.get(StatusQuarto, status_id)

    def buscar_por_descricao(self, descricao: str) -> StatusQuarto | None:
        return self.db.scalar(select(StatusQuarto).where(StatusQuarto.descricao == descricao))


class QuartoRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def listar(self) -> list[Quarto]:
        stmt = select(Quarto).options(joinedload(Quarto.tipo), joinedload(Quarto.status)).order_by(Quarto.numero)
        return list(self.db.scalars(stmt).all())

    def buscar_por_numero(self, numero: str) -> Quarto | None:
        stmt = (
            select(Quarto)
            .options(joinedload(Quarto.tipo), joinedload(Quarto.status))
            .where(Quarto.numero == numero)
        )
        return self.db.scalar(stmt)

    def existe_numero(self, numero: str) -> bool:
        return self.db.scalar(select(Quarto.numero).where(Quarto.numero == numero)) is not None

    def adicionar(self, quarto: Quarto) -> Quarto:
        self.db.add(quarto)
        self.db.flush()
        return self.buscar_por_numero(quarto.numero) or quarto

    def listar_disponiveis(self, data_entrada: date, data_saida: date) -> list[Quarto]:
        stmt = (
            select(Quarto)
            .join(Quarto.status)
            .options(joinedload(Quarto.tipo), joinedload(Quarto.status))
            .where(
                Quarto.ativo.is_(True),
                StatusQuarto.descricao == "DISPONIVEL",
                ~Quarto.numero.in_(
                    select(Reserva.quarto_numero).where(
                        Reserva.status.in_(STATUS_RESERVAS_BLOQUEANTES),
                        Reserva.data_entrada < data_saida,
                        Reserva.data_saida > data_entrada,
                    )
                ),
            )
            .order_by(Quarto.numero)
        )
        return list(self.db.scalars(stmt).all())

    def salvar(self) -> None:
        self.db.commit()

import uuid

from sqlalchemy import Uuid, String, ForeignKey, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models import Base


class User(Base):
	__tablename__ = "users"
	__table_args__ = {"comment": "Таблица пользователей бота (участники, админы, модераторы)"}

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	telegram_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, comment="Telegram id пользователя")

	full_name: Mapped[str] = mapped_column(String(255), nullable=False, comment="ФИО")
	balance: Mapped[float] = mapped_column(Float, default=0, comment="баланс (мнимые единицы)")

	code: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4, comment="код человека (для qr)")
	privileges_id = mapped_column(Integer, ForeignKey("privileges.id"), nullable=True, comment="привилегии пользователя (null - их нет)")

	privileges = relationship("Privilege", back_populates="user", uselist=False)
	created_applies = relationship("PkApply", back_populates="created_by", foreign_keys="[PkApply.created_by_id]")
	promocode_activations = relationship("PromocodeActivation", back_populates="recipient")

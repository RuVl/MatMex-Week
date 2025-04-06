import uuid

from sqlalchemy import Uuid, String, ForeignKey, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from database.models import Base


class User(Base):
	__tablename__ = "users"
	__table_args__ = {"comment": "Таблица пользователей бота (участники, админы, модераторы)"}

	id: Mapped[int] = mapped_column(Integer, primary_key=True)

	full_name: Mapped[str] = mapped_column(String(250), nullable=False, comment="ФИО")
	balance: Mapped[float] = mapped_column(Float, default=0, comment="баланс (мнимые единицы)")

	code: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4, comment="код человека (для qr)")
	privileges_id = mapped_column(Integer, ForeignKey("privileges.id"), nullable=True, comment="привилегии пользователя (null - их нет)")

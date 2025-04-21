import uuid

from sqlalchemy import ForeignKey, Integer, String, Uuid, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models import Base, EventAttendance, EventPrivilegeGrant, PkApply, Privilege, PromocodeActivation, Purchase


class User(Base):
	__tablename__ = "users"
	__table_args__ = {"comment": "Таблица пользователей бота (участники, админы, модераторы)"}

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, comment="Telegram id пользователя")
	telegram_username: Mapped[str] = mapped_column(String(255), nullable=True, comment="Telegram username пользователя")

	full_name: Mapped[str] = mapped_column(String(255), nullable=False, comment="ФИО")
	balance: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="баланс (мнимые единицы)")

	code: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4, comment="код человека (для qr)")

	privileges_id: Mapped[int] = mapped_column(Integer, ForeignKey('privileges.id'), unique=True, nullable=True, comment="привилегии пользователя (null - их нет)")
	privileges: Mapped['Privilege'] = relationship('Privilege', back_populates='owner', foreign_keys=[privileges_id])

	# Back ref pk_applies.created_by_id -> users.id
	apply: Mapped['PkApply'] = relationship('PkApply', back_populates="creator")

	# Back ref purchases.customer_id -> users.id
	purchases: Mapped[list['Purchase']] = relationship('Purchase', back_populates='customer')

	# Back ref promocode_activations.recipient_id -> users.id
	promocode_activations: Mapped[list['PromocodeActivation']] = relationship("PromocodeActivation", back_populates="recipient")

	# Отношение к посещаемости мероприятий
	event_attendances: Mapped[list["EventAttendance"]] = relationship("EventAttendance", back_populates="user")

	# Back ref event_privileges.responsible_id -> users.id
	event_privileges: Mapped[list['EventPrivilegeGrant']] = relationship('EventPrivilegeGrant', back_populates='responsible',
		foreign_keys='EventPrivilegeGrant.responsible_id'
	)

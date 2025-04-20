from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models import Base, Event, PkApply, Promocode, User


class Privilege(Base):
	__tablename__ = "privileges"
	__table_args__ = {"comment": "Привилегии пользователя (o2o)"}

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	privilege: Mapped[int] = mapped_column(Integer, nullable=False, comment="привилегии администрирования")

	created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False, comment="дата выдачи привилегий")
	updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False, comment="дата обновления привилегий")

	# Nullable - for first privilege
	provider_id: Mapped[int] = mapped_column(ForeignKey("privileges.id"), nullable=True, comment="кем выданы")
	provider: Mapped['Privilege'] = relationship('Privilege', foreign_keys=[provider_id])

	# Back ref users.privileges_id -> privileges.id
	owner: Mapped['User'] = relationship('User', back_populates='privileges', uselist=False)

	# Back ref pk_applies.reviewed_by_id -> privileges.id
	reviewed_applies: Mapped[list['PkApply']] = relationship('PkApply', back_populates='reviewed_by')

	# Back ref promocodes.creator_id -> privileges.id
	created_promocodes: Mapped[list['Promocode']] = relationship('Promocode', back_populates='creator')

	# Back ref events.created_by_id -> privileges.id
	created_events: Mapped[list['Event']] = relationship('Event', back_populates='creator')

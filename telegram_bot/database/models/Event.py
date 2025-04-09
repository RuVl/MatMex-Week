from datetime import datetime

from sqlalchemy import DateTime, Integer, String, ForeignKey, func
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.models import Base, Privilege
from database.models import EventPrivilegeGrant


class Event(Base):
	__tablename__ = "events"
	__table_args__ = {"comment": "Проводимые мероприятия"}

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	name: Mapped[str] = mapped_column(String(255), nullable=False, comment="название мероприятия")

	# Может быть всегда начат или никогда не заканчиваться
	starts_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="время начала мероприятия")
	ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="время окончания мероприятия")

	# Кто создал мероприятие
	creator_id: Mapped[int] = mapped_column(Integer, ForeignKey('privileges.id'), nullable=False, comment="кем создан")
	creator: Mapped['Privilege'] = relationship('Privilege', back_populates='created_events', foreign_keys=[creator_id])

	created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment="когда создан")

	# Back ref events.created_by_id -> privileges.id
	event_grants: Mapped[list['EventPrivilegeGrant']] = relationship('EventPrivilegeGrant', back_populates='event')

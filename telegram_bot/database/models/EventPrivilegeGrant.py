from sqlalchemy import ForeignKey, Integer, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.enums import EventPrivilege
from database.models import Base, Event, Privilege


class EventPrivilegeGrant(Base):
	__tablename__ = "event_privileges"
	__table_args__ = {"comment": "Привилегии на конкретное мероприятие"}

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	privileges: Mapped[int] = mapped_column(Enum(EventPrivilege), nullable=False, comment="флаги привилегий")

	# Кто дал права - no backref
	promoter_id: Mapped[int] = mapped_column(Integer, ForeignKey("privileges.id"), nullable=False, comment="кем выданы")
	promoter: Mapped['Privilege'] = relationship('Privilege', foreign_keys=[promoter_id])

	# Кто ответственный
	responsible_id: Mapped[int] = mapped_column(Integer, ForeignKey("privileges.id"), nullable=False, comment="кому предназначено")
	responsible: Mapped['Privilege'] = relationship('Privilege', back_populates='event_privileges', foreign_keys=[responsible_id])

	# За какое мероприятие ответственен
	event_id: Mapped[int] = mapped_column(Integer, ForeignKey('events.id'), nullable=False, comment="на какое мероприятие")
	event: Mapped['Event'] = relationship('Event', back_populates='event_grants', foreign_keys=[event_id])

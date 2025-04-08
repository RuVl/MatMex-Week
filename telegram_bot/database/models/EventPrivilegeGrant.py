from sqlalchemy import ForeignKey, Integer, Enum
from sqlalchemy.orm import mapped_column, Mapped

from database.enums import EventPrivilege
from database.models import Base


class EventPrivilegeGrant(Base):
	__tablename__ = "event_privileges"
	__table_args__ = {"comment": "Привилегии на конкретное мероприятие"}

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	privileges: Mapped[EventPrivilege] = mapped_column(Enum(EventPrivilege), nullable=False, comment="флаги привилегий")
	promoted_by_id: Mapped[int] = mapped_column(Integer, ForeignKey("privileges.id"), nullable=False, comment="кем выданы")
	responsible_id: Mapped[int] = mapped_column(Integer, ForeignKey("privileges.id"), nullable=False, comment="кому предназначено")
	event_id: Mapped[int] = mapped_column(Integer, ForeignKey("events.id"), nullable=False, comment="на какое мероприятие")

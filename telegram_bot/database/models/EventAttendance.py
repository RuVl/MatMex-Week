from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models import Base, Event, User


class EventAttendance(Base):
	__tablename__ = "event_attendances"

	created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment="когда создан")
	points: Mapped[int] = mapped_column(Integer, nullable=False, comment='сколько начислено')

	user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
	user: Mapped["User"] = relationship("User", back_populates="event_attendances")

	event_id: Mapped[int] = mapped_column(Integer, ForeignKey("events.id"), primary_key=True)
	event: Mapped["Event"] = relationship("Event", back_populates="event_attendances")

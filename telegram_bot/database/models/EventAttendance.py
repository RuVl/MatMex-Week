from datetime import datetime

from sqlalchemy import ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models import User, Base, Event


class EventAttendance(Base):
	__tablename__ = "event_attendance"

	user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
	event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), primary_key=True)
	attended: Mapped[bool] = mapped_column(Boolean, default=False, comment="Посетил ли пользователь мероприятие")
	created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False,
	                                             comment="когда создан")

	user: Mapped["User"] = relationship(back_populates="event_attendances")
	event: Mapped["Event"] = relationship(back_populates="event_attendances")

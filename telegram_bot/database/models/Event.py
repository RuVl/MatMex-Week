from datetime import datetime

from sqlalchemy import DateTime, Integer, String, ForeignKey, func
from sqlalchemy.orm import mapped_column, Mapped

from database.models import Base


class Event(Base):
	__tablename__ = "events"
	__table_args__ = {"comment": "Проводимые мероприятия"}

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	name: Mapped[str] = mapped_column(String(250), nullable=False, comment="название мероприятия")

	created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment="когда создан")
	created_by_id: Mapped[int] = mapped_column(Integer, ForeignKey("privileges.id"), nullable=False, comment="кем создан")

	starts_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="время начала мероприятия")
	ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="время окончания мероприятия")

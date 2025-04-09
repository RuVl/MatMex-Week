from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.enums import ApplyStatus
from database.models import Base, User, Privilege


class PkApply(Base):
	__tablename__ = "pk_applies"
	__table_args__ = {"comment": "Заявки на ручную проверку статуса"}

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	status: Mapped[str] = mapped_column(Enum(ApplyStatus), default=ApplyStatus.pending, nullable=False, comment="статус заявки")
	reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="когда рассмотрена")

	# Связь с пользователем, создавшим заявку
	creator_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), unique=True, nullable=False, comment="кто подал заявку")
	creator: Mapped['User'] = relationship('User', back_populates='apply', foreign_keys=[creator_id])

	# Связь с привилегией, рассмотревшей заявку
	reviewed_by_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("privileges.id"), nullable=True, comment="кем рассмотрена")
	reviewed_by: Mapped['Privilege'] = relationship('Privilege', back_populates="reviewed_applies", foreign_keys=[reviewed_by_id])

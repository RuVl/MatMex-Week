from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.enums import ApplyStatus
from database.models import Base


class PkApply(Base):
	__tablename__ = "pk_applies"
	__table_args__ = {"comment": "Заявки на ручную проверку статуса"}

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	status: Mapped[ApplyStatus] = mapped_column(Enum(ApplyStatus), default=ApplyStatus.pending, nullable=False, comment="статус заявки")

	reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="когда рассмотрена")
	reviewed_by_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True, comment="кем рассмотрена")

	created_by_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, comment="кто подал заявку")

	# Связь с пользователем, создавшим заявку
	created_by = relationship("User", back_populates="created_applies", foreign_keys=[created_by_id])

	# Связь с пользователем, рассмотревшим заявку
	reviewed_by = relationship("User", back_populates="reviewed_applies", foreign_keys=[reviewed_by_id])

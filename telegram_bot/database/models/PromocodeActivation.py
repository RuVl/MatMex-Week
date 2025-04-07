from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, func, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.models import Base


class PromocodeActivation(Base):
	__tablename__ = "promocode_activations"
	__table_args__ = (
		{"comment": "Активация промокодов (m2m)"},
		UniqueConstraint("promocode_id", "recipient_id", name="uq_promocode_recipient")
	)

	id: Mapped[int] = mapped_column(primary_key=True)

	promocode_id: Mapped[int] = mapped_column(Integer, ForeignKey("promocodes.id"), nullable=False, comment="какой промокод активировали")
	recipient_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, comment="кто активировал")

	activated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment="когда активировали")

	promocode = relationship("Promocode", back_populates="activations")
	recipient = relationship("User", back_populates="promocode_activations")
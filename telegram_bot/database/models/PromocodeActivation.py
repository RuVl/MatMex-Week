from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models import Base, Promocode, User


class PromocodeActivation(Base):
	__tablename__ = "promocode_activations"
	__table_args__ = {"comment": "Активация промокодов (m2m)"}

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	activated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment="когда активировали")
	points: Mapped[int] = mapped_column(Integer, nullable=False, comment='сколько начислено')

	# Какой промокод активировали
	promocode_id: Mapped[int] = mapped_column(Integer, ForeignKey('promocodes.id'), nullable=False, comment="какой промокод активировали")
	promocode: Mapped['Promocode'] = relationship("Promocode", back_populates="activations", foreign_keys=[promocode_id])

	# Кто активировал
	recipient_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False, comment="кто активировал")
	recipient: Mapped['User'] = relationship('User', back_populates="promocode_activations", foreign_keys=[recipient_id])

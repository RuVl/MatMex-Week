from sqlalchemy import ForeignKey, Integer, Float
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.models import Base, User, MerchItem


class Purchase(Base):
	__tablename__ = "purchases"
	__table_args__ = {"comment": "Информация о покупках пользователя"}

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	quantity: Mapped[int] = mapped_column(Integer, nullable=False, comment="количество экземпляров")
	total_cost: Mapped[float] = mapped_column(Float, nullable=False, comment="стоимость покупки")

	# Кто купил мерч
	customer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, comment="кто купил")
	customer: Mapped['User'] = relationship('User', back_populates="purchases", foreign_keys=[customer_id])

	# Какой мерч купили - no backref (думаю мерчу не должен ссылаться на покупки)
	merch_id: Mapped[int] = mapped_column(Integer, ForeignKey("merch_items.id"), unique=True, nullable=False, comment="что купили")
	merch: Mapped['MerchItem'] = relationship('MerchItem', foreign_keys=[merch_id])

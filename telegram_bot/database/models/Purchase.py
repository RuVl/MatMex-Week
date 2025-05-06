from sqlalchemy import ForeignKey, Integer
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.enums import ApplyStatus
from database.models import Base, MerchItem, User


class Purchase(Base):
	__tablename__ = "purchases"
	__table_args__ = {"comment": "Информация о покупках пользователя"}

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	status: Mapped[ApplyStatus] = mapped_column(
		postgresql.ENUM(ApplyStatus), default=ApplyStatus.PENDING.value, nullable=True, comment="статус покупки"
	)
	quantity: Mapped[int] = mapped_column(Integer, nullable=False, comment="количество экземпляров")
	total_cost: Mapped[int] = mapped_column(Integer, nullable=False, comment="стоимость покупки")

	# Кто купил мерч
	customer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, comment="кто купил")
	customer: Mapped['User'] = relationship('User', back_populates="purchases", foreign_keys=[customer_id])

	# Какой мерч купили - no backref (думаю мерчу не должен ссылаться на покупки)
	merch_id: Mapped[int] = mapped_column(Integer, ForeignKey("merch_items.id"), nullable=False, comment="что купили")
	merch: Mapped['MerchItem'] = relationship('MerchItem', foreign_keys=[merch_id])

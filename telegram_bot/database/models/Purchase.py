from sqlalchemy import ForeignKey, Integer, Float
from sqlalchemy.orm import mapped_column, Mapped

from database.models import Base


class Purchase(Base):
	__tablename__ = "purchases"
	__table_args__ = {"comment": "Информация о покупках пользователя"}

	id: Mapped[int] = mapped_column(Integer, primary_key=True)

	customer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, comment="кто купил")
	merch_id: Mapped[int] = mapped_column(Integer, ForeignKey("merch_items.id"), nullable=False, comment="что купили")

	quantity: Mapped[int] = mapped_column(Integer, nullable=False, comment="количество экземпляров")
	total_cost: Mapped[float] = mapped_column(Float, nullable=False, comment="стоимость покупки")

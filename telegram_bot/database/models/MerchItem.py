from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.enums import MerchSize
from database.models import Base, MerchCategory


class MerchItem(Base):
	__tablename__ = "merch_items"
	__table_args__ = {"comment": "Товарная единица определенного размера"}

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	image_path: Mapped[str] = mapped_column(String(255), nullable=False)

	name: Mapped[str] = mapped_column(String(255), nullable=False, comment="название товара")
	description: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="описание товара")
	size: Mapped[MerchSize] = mapped_column(postgresql.ENUM(MerchSize), nullable=False, comment="размер товара")

	full_price: Mapped[int] = mapped_column(Integer, nullable=False, comment="цена без скидки")
	discount_price: Mapped[int] = mapped_column(Integer, nullable=False, comment="стоимость со скидкой")

	available_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="сколько доступно")
	in_stock: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, comment="активна ли продажа")

	category_id: Mapped[int] = mapped_column(Integer, ForeignKey("merch_categories.id"), nullable=False, comment="к какой категории относится")
	category: Mapped['MerchCategory'] = relationship('MerchCategory', back_populates='merch_items', foreign_keys=[category_id])

	def full_name(self) -> str:
		return self.name if self.size.value == MerchSize.NONE else f"{self.name} {self.size.value}"

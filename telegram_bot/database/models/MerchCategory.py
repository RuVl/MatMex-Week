from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models import Base, MerchItem


class MerchCategory(Base):
	__tablename__ = "merch_categories"
	__table_args__ = {"comment": "Категория мерча"}

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	name: Mapped[str] = mapped_column(String(255), nullable=False, comment="название группы товаров")
	image_path: Mapped[str] = mapped_column(String(255), nullable=False)

	# Back ref merch_items.category_id -> merch_categories.id
	merch_items: Mapped[list['MerchItem']] = relationship('MerchItem', back_populates='category')

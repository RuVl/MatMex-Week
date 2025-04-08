from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column, Mapped

from database.models import Base


class MerchCategory(Base):
	__tablename__ = "merch_categories"
	__table_args__ = {"comment": "Категория мерча (Футболки)"}

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	name: Mapped[str] = mapped_column(String(255), nullable=False, comment="название группы товаров")
	image_path: Mapped[str] = mapped_column(String(255), nullable=False)

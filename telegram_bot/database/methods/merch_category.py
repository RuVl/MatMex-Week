from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import MerchCategory, MerchItem


async def create_merch_category(session: AsyncSession, name: str) -> MerchCategory:
	"""Создаёт новую категорию товаров."""
	category = MerchCategory(name=name)
	session.add(category)
	await session.commit()
	return category


async def get_all_categories(session: AsyncSession) -> list[MerchCategory]:
	"""Возвращает список всех категорий."""
	result = await session.execute(select(MerchCategory))
	return result.scalars().all()


async def get_merch_by_category(session: AsyncSession, category_id: int) -> list[MerchItem]:
	"""Возвращает список товаров в указанной категории."""
	result = await session.execute(select(MerchItem).where(MerchItem.category_id == category_id))
	return result.scalars().all()

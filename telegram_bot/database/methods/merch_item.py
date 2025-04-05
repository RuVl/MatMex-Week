from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models import MerchItem


async def create_merch_item(session: AsyncSession, merch_name: str, price: int, stock: int,
							category_id: int) -> MerchItem:
	"""Создаёт новый товар."""
	item = MerchItem(merch_name=merch_name, price=price, stock=stock, category_id=category_id)
	session.add(item)
	await session.commit()
	return item


async def get_merch_item_by_id(session: AsyncSession, item_id: int) -> MerchItem | None:
	"""Возвращает товар по ID или None, если не найден."""
	return await session.get(MerchItem, item_id)


async def update_merch_stock(session: AsyncSession, item_id: int, quantity: int):
	"""Обновляет количество товара."""
	await session.execute(
		update(MerchItem).where(MerchItem.id == item_id).values(stock=MerchItem.stock + quantity)
	)
	await session.commit()


async def get_available_merch_items(session: AsyncSession) -> list[MerchItem]:
	"""Возвращает список доступных товаров."""
	result = await session.execute(select(MerchItem).where(MerchItem.is_available, MerchItem.stock > 0))
	return result.scalars().all()

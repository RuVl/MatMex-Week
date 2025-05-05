import os

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import MerchItem


async def create_item(
		session: AsyncSession,
		name: str,
		description: str | None,
		image_path: str,
		size: str,
		full_price: float,
		discount_price: float,
		available_count: int,
		in_stock: bool,
		category_id: int
) -> MerchItem:
	item = MerchItem(
		name=name,
		description=description,
		image_path=image_path,
		size=size,
		full_price=full_price,
		discount_price=discount_price,
		available_count=available_count,
		in_stock=in_stock,
		category_id=category_id
	)
	session.add(item)

	await session.commit()
	await session.refresh(item)

	return item


async def get_item_by_id(session: AsyncSession, item_id: int) -> MerchItem | None:
	query = (
		select(MerchItem)
		.where(MerchItem.id == item_id)
	)
	result = await session.execute(query)
	return result.scalars().first()


async def get_all_items(session: AsyncSession) -> list[MerchItem]:
	"""Get all merch items from the database"""
	query = select(MerchItem)
	result = await session.execute(query)
	return list(result.scalars().all())


async def remove_item_by_id(session: AsyncSession, item_id: int) -> bool:
	item = await get_item_by_id(session, item_id)

	if item:
		if os.path.exists(item.image_path):
			os.remove(item.image_path)

		await session.delete(item)
		await session.commit()

		return True

	return False

import os
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.models import MerchCategory
from .merch_item import remove_item_by_id


async def get_all_categories(session: AsyncSession) -> list[MerchCategory]:
	result = await session.execute(
		select(MerchCategory)
	)
	return result.scalars().all()


async def create_category(session: AsyncSession, name: str, image_path: str) -> MerchCategory:
	category = MerchCategory(name=name, image_path=image_path)
	session.add(category)
	await session.commit()
	await session.refresh(category)
	return category


async def get_category_by_id(session: AsyncSession, category_id: int) -> MerchCategory | None:
	query = (
		select(MerchCategory)
		.where(MerchCategory.id == category_id)
		.options(selectinload(MerchCategory.merch_items))
	)
	result = await session.execute(query)
	return result.scalars().first()


async def remove_category_by_id(session: AsyncSession, category_id: int) -> bool:
	category = await get_category_by_id(session, category_id)
	if category:
		if os.path.exists(category.image_path):
			os.remove(category.image_path)
		for item in category.merch_items:
			await remove_item_by_id(session, item.id)
		await session.delete(category)
		await session.commit()
		return True
	return False

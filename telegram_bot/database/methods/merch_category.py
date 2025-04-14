import os
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from database.models import MerchCategory
from .merch_item import remove_item

async def get_all_categories(session: AsyncSession) -> list[MerchCategory]:
	"""Создаёт заявку на привилегированный статус."""
	result = await session.execute(
		select(MerchCategory)
	)
	return result.scalars().all()

async def create_category(session: AsyncSession, name : str, image_path : str) -> MerchCategory | None:
	"""Создаёт заявку на привилегированный статус."""
	category = MerchCategory(name = name, image_path = image_path)
	session.add(category)
	try:
		await session.commit()
		await session.refresh(category)
		return category
	except IntegrityError:
		await session.rollback()
		return None

async def get_category(session: AsyncSession, name : str) -> MerchCategory | None:
	query = (
		select(MerchCategory)
		.where(MerchCategory.name == name)
		.options(selectinload(MerchCategory.merch_items))
	)
	result = await session.execute(query)
	return result.scalars().first()

async def remove_category(session: AsyncSession, category: MerchCategory) -> bool:
	if category:
		if os.path.exists(category.image_path):
			os.remove(category.image_path)
		for item in category.merch_items:
			await remove_item(session, item)
		await session.delete(category)
		await session.commit()
		return True
	return False


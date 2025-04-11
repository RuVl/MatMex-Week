from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.models import MerchCategory


async def get_all_categories(session: AsyncSession) -> list[MerchCategory]:
	"""Создаёт заявку на привилегированный статус."""
	result = await session.execute(
		select(MerchCategory)
	)
	return result.scalars().all()

async def create_category(session: AsyncSession, name : str, image_path : str) -> MerchCategory:
	"""Создаёт заявку на привилегированный статус."""
	request = MerchCategory(name = name, image_path = image_path)
	session.add(request)
	await session.commit()
	await session.refresh(request)
	return request
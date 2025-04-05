from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from models import Purchase


async def record_purchase(session: AsyncSession, user_id: int, merch_id: int, quantity: int, total_cost: int):
	"""Записывает покупку товара пользователем."""
	purchase = Purchase(user_id=user_id, merch_id=merch_id, quantity=quantity, total_cost=total_cost)
	session.add(purchase)
	await session.commit()


async def get_user_purchases(session: AsyncSession, user_id: int) -> list[Purchase]:
	"""Возвращает историю покупок пользователя."""
	result = await session.execute(select(Purchase).where(Purchase.user_id == user_id))
	return result.scalars().all()


async def get_total_spent_by_user(session: AsyncSession, user_id: int) -> int:
	"""Возвращает общую сумму, потраченную пользователем."""
	result = await session.execute(
		select(func.sum(Purchase.total_cost)).where(Purchase.user_id == user_id)
	)
	return result.scalar_one_or_none() or 0

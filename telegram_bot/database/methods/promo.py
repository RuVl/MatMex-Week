from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sql_func
from sqlalchemy.orm import selectinload
from datetime import datetime

from database.models import Promocode, PromocodeActivation, User


async def create_promocode(
		session: AsyncSession,
		code: str,
		cost: int,
		creator_id: int,
		max_uses: int | None = None,
		expires_at: datetime | None = None
) -> Promocode:
	"""Создаёт новый промокод."""
	promocode = Promocode(
		code=code,
		cost=cost,
		creator_id=creator_id,
		max_uses=max_uses,
		expires_at=expires_at
	)
	session.add(promocode)
	await session.commit()
	await session.refresh(promocode)
	return promocode


async def get_promocode_by_code(session: AsyncSession, code: str) -> Promocode | None:
	"""Возвращает промокод по его коду или None, если не найден."""
	result = await session.execute(
		select(Promocode)
			.where(Promocode.code == code)
	)
	return result.scalar_one_or_none()


async def activate_promocode(session: AsyncSession, promocode_id: int, user_id: int) -> bool:
	"""Активирует промокод для пользователя, если это возможно."""
	promocode = await session.get(Promocode, promocode_id, options=[
		selectinload(Promocode.activations)
	])
	user = await session.get(User, user_id)

	if not promocode or not user:
		return False
	if not promocode.is_active:
		return False
	if promocode.expires_at and promocode.expires_at < datetime.utcnow():
		return False

	# Проверяем количество активаций
	activation_count = len(promocode.activations)
	if promocode.max_uses is not None and activation_count >= promocode.max_uses:
		return False

	# Проверяем, активировал ли пользователь уже этот промокод
	if any(act.recipient_id == user_id for act in promocode.activations):
		return False

	# Создаём активацию
	activation = PromocodeActivation(promocode_id=promocode_id, recipient_id=user_id)
	session.add(activation)
	user.balance += promocode.cost  # Начисляем баллы
	await session.commit()
	return True


async def deactivate_promocode(session: AsyncSession, promocode_id: int):
	"""Деактивирует промокод."""
	promocode = await session.get(Promocode, promocode_id)
	if promocode:
		promocode.is_active = False
		await session.commit()


async def get_promocodes_by_creator(session: AsyncSession, creator_id: int) -> list[Promocode]:
	"""Возвращает список промокодов, созданных указанной привилегией."""
	result = await session.execute(
		select(Promocode)
			.where(Promocode.creator_id == creator_id)
			.options(selectinload(Promocode.activations))
	)
	return result.scalars().all()


async def get_active_promocodes(session: AsyncSession) -> list[Promocode]:
	"""Возвращает список активных промокодов, которые ещё не истекли."""
	result = await session.execute(
		select(Promocode)
			.where(Promocode.is_active == True)
			.where((Promocode.expires_at == None) | (Promocode.expires_at > datetime.utcnow()))
			.options(selectinload(Promocode.activations))
	)
	return result.scalars().all()
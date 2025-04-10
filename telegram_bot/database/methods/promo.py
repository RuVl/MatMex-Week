from datetime import datetime

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

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
	query = (
		select(Promocode)
		.where(Promocode.code == code)
		.options(selectinload(Promocode.activations))
	)
	result = await session.execute(query)
	return result.scalar_one_or_none()


async def check_promocode_valid(session: AsyncSession, code: str, user_id: int) -> tuple[bool, str, int]:
	"""
	Проверяет, действителен ли промокод и может ли пользователь его активировать.
	Возвращает кортеж (is_valid, message, cost):
	- is_valid: True если промокод действителен
	- message: сообщение о результате проверки
	- cost: стоимость промокода (если действителен, иначе 0)
	"""
	promocode = await get_promocode_by_code(session, code)

	if not promocode:
		return False, "Промокод не найден", 0
	
	if not promocode.is_active:
		return False, "Промокод деактивирован", 0
	
	if promocode.expires_at and promocode.expires_at < datetime.utcnow():
		return False, "Срок действия промокода истек", 0
	
	# Проверяем количество активаций
	if promocode.max_uses is not None and len(promocode.activations) >= promocode.max_uses:
		return False, "Достигнуто максимальное количество использований промокода", 0
	
	# Проверяем, активировал ли пользователь уже этот промокод
	query = select(exists().where(
		(PromocodeActivation.promocode_id == promocode.id) &
		(PromocodeActivation.recipient_id == user_id)
	))
	result = await session.execute(query)
	if result.scalar_one():
		return False, "Вы уже активировали этот промокод", 0

	return True, "Промокод действителен", promocode.cost


async def activate_promocode(session: AsyncSession, code: str, user_id: int) -> tuple[bool, str, int]:
	"""
	Активирует промокод для пользователя, если это возможно.
	Возвращает кортеж (success, message, cost):
	- success: True если активация успешна
	- message: сообщение о результате активации
	- cost: начисленные баллы (если успешно, иначе 0)
	"""
	is_valid, message, cost = await check_promocode_valid(session, code, user_id)

	if not is_valid:
		return False, message, 0

	promocode = await get_promocode_by_code(session, code)
	if not promocode:
		return False, "Произошла ошибка при получении промокода", 0

	# Получаем пользователя и обновляем баланс
	user = await session.get(User, user_id)
	if not user:
		return False, "Пользователь не найден", 0
	
	# Создаём активацию
	activation = PromocodeActivation(promocode_id=promocode.id, recipient_id=user_id)
	session.add(activation)

	# Начисляем баллы
	user.balance += promocode.cost
	
	await session.commit()
	return True, f"Промокод активирован! Начислено {promocode.cost} баллов", promocode.cost


async def deactivate_promocode(session: AsyncSession, promocode_id: int) -> bool:
	"""Деактивирует промокод."""
	promocode = await session.get(Promocode, promocode_id)
	if promocode:
		promocode.is_active = False
		await session.commit()
		return True
	return False


async def get_promocodes_by_creator(session: AsyncSession, creator_id: int) -> list[Promocode]:
	"""Возвращает список промокодов, созданных указанной привилегией."""
	query = (
		select(Promocode)
		.where(Promocode.creator_id == creator_id)
		.options(selectinload(Promocode.activations))
	)
	result = await session.execute(query)
	return result.scalars().all()


async def get_active_promocodes(session: AsyncSession) -> list[Promocode]:
	"""Возвращает список активных промокодов, которые ещё не истекли."""
	current_time = datetime.utcnow()
	query = (
		select(Promocode)
		.where(Promocode.is_active == True)
		.where((Promocode.expires_at == None) | (Promocode.expires_at > current_time))
		.options(selectinload(Promocode.activations))
	)
	result = await session.execute(query)
	return result.scalars().all()

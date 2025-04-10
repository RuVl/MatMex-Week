from sqlalchemy import select, exists
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.models import PromocodeActivation


async def create_activation(session: AsyncSession, promocode_id: int, recipient_id: int) -> PromocodeActivation | None:
	"""Создаёт запись об активации промокода."""
	# Проверяем, существует ли уже активация
	query = select(exists().where(
		(PromocodeActivation.promocode_id == promocode_id) &
		(PromocodeActivation.recipient_id == recipient_id)
	))
	result = await session.execute(query)
	if result.scalar_one():
		return None  # Пользователь уже активировал этот промокод

	activation = PromocodeActivation(promocode_id=promocode_id, recipient_id=recipient_id)
	session.add(activation)
	try:
		await session.commit()
		await session.refresh(activation)
		return activation
	except IntegrityError:
		await session.rollback()
		return None  # Произошла ошибка при создании активации


async def get_activation_by_ids(session: AsyncSession, promocode_id: int,
                                recipient_id: int) -> PromocodeActivation | None:
	"""Возвращает запись об активации для промокода и пользователя."""
	query = (
		select(PromocodeActivation)
		.where(PromocodeActivation.promocode_id == promocode_id)
		.where(PromocodeActivation.recipient_id == recipient_id)
		.options(
			selectinload(PromocodeActivation.promocode),
			selectinload(PromocodeActivation.recipient)
		)
	)
	result = await session.execute(query)
	return result.scalar_one_or_none()


async def get_user_activations(session: AsyncSession, recipient_id: int) -> list[PromocodeActivation]:
	"""Возвращает список активаций промокодов для пользователя."""
	query = (
		select(PromocodeActivation)
		.where(PromocodeActivation.recipient_id == recipient_id)
		.options(selectinload(PromocodeActivation.promocode))
	)
	result = await session.execute(query)
	return result.scalars().all()


async def get_recent_user_activations(session: AsyncSession, recipient_id: int, limit: int = 5) -> list[PromocodeActivation]:
	"""Возвращает список последних активаций промокодов для пользователя."""
	query = (
		select(PromocodeActivation)
		.where(PromocodeActivation.recipient_id == recipient_id)
		.options(selectinload(PromocodeActivation.promocode))
		.order_by(PromocodeActivation.activated_at.desc())
		.limit(limit)
	)
	result = await session.execute(query)
	return result.scalars().all()


async def get_promocode_activations(session: AsyncSession, promocode_id: int) -> list[PromocodeActivation]:
	"""Возвращает список активаций указанного промокода."""
	query = (
		select(PromocodeActivation)
		.where(PromocodeActivation.promocode_id == promocode_id)
		.options(selectinload(PromocodeActivation.recipient))
	)
	result = await session.execute(query)
	return result.scalars().all()


async def get_user_activation_count(session: AsyncSession, recipient_id: int) -> int:
	"""Возвращает количество активированных пользователем промокодов."""
	query = (
		select(PromocodeActivation)
		.where(PromocodeActivation.recipient_id == recipient_id)
	)
	result = await session.execute(query)
	return len(result.scalars().all())

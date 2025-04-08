from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.models import PromocodeActivation, Promocode, User


async def create_activation(session: AsyncSession, promocode_id: int, recipient_id: int) -> PromocodeActivation | None:
	"""Создаёт запись об активации промокода."""
	activation = PromocodeActivation(promocode_id=promocode_id, recipient_id=recipient_id)
	session.add(activation)
	try:
		await session.commit()
		await session.refresh(activation)
		return activation
	except IntegrityError:
		await session.rollback()
		return None  # Пользователь уже активировал этот промокод


async def get_activation_by_ids(session: AsyncSession, promocode_id: int,
                                recipient_id: int) -> PromocodeActivation | None:
	"""Возвращает запись об активации для промокода и пользователя."""
	result = await session.execute(
		select(PromocodeActivation)
		.where(PromocodeActivation.promocode_id == promocode_id)
		.where(PromocodeActivation.recipient_id == recipient_id)
		.options(
			selectinload(PromocodeActivation.promocode),
			selectinload(PromocodeActivation.recipient)
		)
	)
	return result.scalar_one_or_none()


async def get_user_activations(session: AsyncSession, recipient_id: int) -> list[PromocodeActivation]:
	"""Возвращает список активаций промокодов для пользователя."""
	result = await session.execute(
		select(PromocodeActivation)
		.where(PromocodeActivation.recipient_id == recipient_id)
		.options(selectinload(PromocodeActivation.promocode))
	)
	return result.scalars().all()


async def get_promocode_activations(session: AsyncSession, promocode_id: int) -> list[PromocodeActivation]:
	"""Возвращает список активаций указанного промокода."""
	result = await session.execute(
		select(PromocodeActivation)
		.where(PromocodeActivation.promocode_id == promocode_id)
		.options(selectinload(PromocodeActivation.recipient))
	)
	return result.scalars().all()


async def activate_promocode(session: AsyncSession, promocode_id: int, recipient_id: int) -> bool:
	"""Активирует промокод для пользователя с учётом всех условий."""
	promocode = await session.get(Promocode, promocode_id, options=[selectinload(Promocode.activations)])
	user = await session.get(User, recipient_id)

	if not promocode or not user:
		return False
	if not promocode.is_active:
		return False
	if promocode.expires_at and promocode.expires_at < datetime.utcnow():
		return False
	if promocode.max_uses is not None and len(promocode.activations) >= promocode.max_uses:
		return False

	# Пробуем создать активацию
	activation = await create_activation(session, promocode_id, recipient_id)
	if activation:
		user.balance += promocode.cost  # Начисляем баллы
		await session.commit()
		return True
	return False  # Активация не удалась (например, уже активирован)

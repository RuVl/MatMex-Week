from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import PromoActivation


async def record_promo_activation(session: AsyncSession, user_id: int, promo_id: int):
	"""Записывает активацию промокода пользователем."""
	activation = PromoActivation(user_id=user_id, promo_id=promo_id)
	session.add(activation)
	await session.commit()


async def has_activated_promo(session: AsyncSession, user_id: int, promo_id: int) -> bool:
	"""Проверяет, активировал ли пользователь указанный промокод."""
	result = await session.execute(
		select(PromoActivation).where(PromoActivation.user_id == user_id, PromoActivation.promo_id == promo_id)
	)
	return result.scalar_one_or_none() is not None


async def get_user_activations(session: AsyncSession, user_id: int) -> list[PromoActivation]:
	"""Возвращает список всех активаций промокодов пользователя."""
	result = await session.execute(select(PromoActivation).where(PromoActivation.user_id == user_id))
	return result.scalars().all()


async def get_users_by_code(session: AsyncSession, promo_id: int) -> list[PromoActivation]:
	"""Возвращает список всех пользователей, активировавших промокод."""
	result = await session.execute(select(PromoActivation).where(PromoActivation.promo_id == promo_id))
	return result.scalars().all()

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import PromoCode


async def create_promo_code(
		session: AsyncSession,
		code: str,
		value: int,
		creator_id: int,
		expires_at=None,
		max_uses=10000,
) -> PromoCode:
	"""Создаёт новый промокод."""
	promo = PromoCode(
		code=code,
		value=value,
		is_active=True,
		creator_id=creator_id,
		expires_at=expires_at,
		max_uses=max_uses,
	)
	session.add(promo)
	await session.commit()
	return promo


async def get_promo_code_by_code(session: AsyncSession, code: str) -> PromoCode | None:
	"""Возвращает промокод по его значению или None, если не найден."""
	result = await session.execute(select(PromoCode).where(PromoCode.code == code))
	return result.scalar_one_or_none()


async def activate_promo_code(session: AsyncSession, promo_id: int):
	"""Увеличивает счётчик использований промокода."""
	await session.execute(
		update(PromoCode).where(PromoCode.id == promo_id).values(used_count=PromoCode.used_count + 1)
	)
	await session.commit()


async def deactivate_promo_code(session: AsyncSession, promo_id: int):
	"""Деактивирует промокод."""
	await session.execute(
		update(PromoCode).where(PromoCode.id == promo_id).values(is_active=False)
	)
	await session.commit()

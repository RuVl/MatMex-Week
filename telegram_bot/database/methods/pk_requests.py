from datetime import datetime, UTC

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import PKRequests


async def create_privilege_request(session: AsyncSession, user_id: int):
	"""Создаёт заявку на привилегированный статус."""
	request = PKRequests(user_id=user_id)
	session.add(request)
	await session.commit()


async def update_request_status(session: AsyncSession, request_id: int, status: str, reviewed_by: int):
	"""Обновляет статус заявки."""
	await session.execute(
		update(PKRequests)
			.where(PKRequests.id == request_id)
		.values(status=status, reviewed_at=datetime.now(UTC), reviewed_by=reviewed_by)
	)
	await session.commit()


async def get_pending_requests(session: AsyncSession) -> list[PKRequests]:
	"""Возвращает список заявок со статусом 'pending'."""
	result = await session.execute(select(PKRequests).where(PKRequests.status == "pending"))
	return result.scalars().all()


async def get_user_request(session: AsyncSession, user_id: int) -> PKRequests | None:
	"""Возвращает заявку пользователя или None, если не найдена."""
	result = await session.execute(select(PKRequests).where(PKRequests.user_id == user_id))
	return result.scalar_one_or_none()

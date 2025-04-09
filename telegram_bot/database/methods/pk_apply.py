from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.enums import ApplyStatus
from database.models import PkApply


async def create_privilege_request(session: AsyncSession, creator_id: int) -> PkApply:
	"""Создаёт заявку на привилегированный статус."""
	request = PkApply(creator_id=creator_id)
	session.add(request)
	await session.commit()
	await session.refresh(request)
	return request


async def update_request_status(session: AsyncSession, request_id: int, status: ApplyStatus, reviewed_by_id: int) -> PkApply:
	"""Обновляет статус заявки."""
	request = await session.get(PkApply, request_id, options=[
		selectinload(PkApply.creator),
		selectinload(PkApply.reviewed_by)
	])
	if request:
		request.status = status
		request.reviewed_by_id = reviewed_by_id
		request.reviewed_at = datetime.utcnow()
		await session.commit()
		return request
	else:
		raise ValueError(f"Заявка с id {request_id} не найдена")


async def get_pending_requests(session: AsyncSession) -> list[PkApply]:
	"""Возвращает список заявок со статусом 'pending' с данными о создателях."""
	result = await session.execute(
		select(PkApply)
		.where(PkApply.status == ApplyStatus.pending)
		.options(selectinload(PkApply.creator))
	)
	return result.scalars().all()


async def get_user_request(session: AsyncSession, created_by_id: int) -> PkApply | None:
	"""Возвращает последнюю заявку пользователя или None, если не найдена."""
	result = await session.execute(
		select(PkApply)
		.where(PkApply.creator_id == created_by_id)
		.options(
			selectinload(PkApply.creator),
			selectinload(PkApply.reviewed_by)
		)
		.order_by(PkApply.id.desc())  # Последняя заявка по ID
	)
	return result.scalar_one_or_none()


async def get_requests_by_reviewer(session: AsyncSession, reviewed_by_id: int) -> list[PkApply]:
	"""Возвращает список заявок, рассмотренных указанным пользователем."""
	result = await session.execute(
		select(PkApply)
		.where(PkApply.reviewed_by_id == reviewed_by_id)
		.options(
			selectinload(PkApply.creator),
			selectinload(PkApply.reviewed_by)
		)
	)
	return result.scalars().all()

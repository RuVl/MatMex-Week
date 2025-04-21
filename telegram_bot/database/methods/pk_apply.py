from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.enums import ApplyStatus
from database.models import PkApply


async def create_apply(session: AsyncSession, creator_id: int) -> PkApply:
	"""Создаёт заявку на привилегированный статус."""
	request = PkApply(creator_id=creator_id)
	session.add(request)
	await session.commit()
	await session.refresh(request)
	return request


async def delete_apply(session: AsyncSession, apply_id: int) -> bool:
	"""Deletes apply if exists."""
	result = await session.execute(
		select(PkApply)
		.where(PkApply.id == apply_id)
	)
	apply = result.scalar_one_or_none()

	if not apply:
		return False

	await session.delete(apply)
	await session.commit()
	return True


async def update_apply_status(session: AsyncSession, apply_id: int, status: ApplyStatus, reviewed_by_id: int) -> PkApply:
	"""Обновляет статус заявки."""
	request = await session.get(PkApply, apply_id, options=[
		selectinload(PkApply.creator),
		selectinload(PkApply.reviewed_by)
	])
	if request:
		request.status = status
		request.reviewed_by_id = reviewed_by_id
		request.reviewed_at = datetime.now(timezone.utc)
		await session.commit()
		return request
	else:
		raise ValueError(f"Заявка с id {apply_id} не найдена")


async def get_pending_applies(session: AsyncSession) -> list[PkApply]:
	"""Возвращает список заявок со статусом 'pending' с данными о создателях."""
	result = await session.execute(
		select(PkApply)
		.where(PkApply.status == ApplyStatus.PENDING)
		.options(selectinload(PkApply.creator))
	)
	return result.scalars().all()


async def get_user_apply(session: AsyncSession, created_by_id: int) -> PkApply | None:
	"""Возвращает заявку пользователя или None, если не найдена."""
	result = await session.execute(
		select(PkApply)
		.where(PkApply.creator_id == created_by_id)
		.options(
			selectinload(PkApply.creator),
			selectinload(PkApply.reviewed_by)
		)
	)
	return result.scalar_one_or_none()


async def get_applies_by_reviewer(session: AsyncSession, reviewed_by_id: int) -> list[PkApply]:
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

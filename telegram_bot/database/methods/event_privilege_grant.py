from datetime import timezone, datetime

from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.enums import EventPrivilege
from database.models import EventPrivilegeGrant, Event


async def add_event_privilege_grant(
		session: AsyncSession,
		user_id: int,
		privilege_id: int,
		event_id: int,
		privileges: EventPrivilege
) -> EventPrivilegeGrant:
	"""Добавляет пользователю привилегии на мероприятие."""
	grant = EventPrivilegeGrant(
		responsible_id=user_id,
		promoter_id=privilege_id,
		event_id=event_id,
		privileges=privileges
	)
	session.add(grant)
	await session.commit()
	await session.refresh(grant)
	return grant


async def update_event_privilege_grant(
		session: AsyncSession,
		grant_id: int,
		privileges: EventPrivilege
) -> EventPrivilegeGrant:
	"""Обновляет привилегии пользователя на мероприятие."""
	grant = await session.get(EventPrivilegeGrant, grant_id, options=[
		selectinload(EventPrivilegeGrant.event),
		selectinload(EventPrivilegeGrant.responsible),
		selectinload(EventPrivilegeGrant.promoter)
	])
	if grant:
		grant.privileges = privileges
		await session.commit()
		return grant
	else:
		raise ValueError(f"Привилегия с id {grant_id} не найдена")


async def delete_event_privilege_grant(session: AsyncSession, grant_id: int) -> bool:
	"""Удаляет привилегию пользователя на мероприятие."""
	grant = await session.get(EventPrivilegeGrant, grant_id)
	if grant:
		await session.delete(grant)
		await session.commit()
		return True
	return False


async def get_user_event_grants(session: AsyncSession, user_id: int) -> list[EventPrivilegeGrant]:
	"""Возвращает список привилегий пользователя на мероприятия."""
	result = await session.execute(
		select(EventPrivilegeGrant)
		.where(EventPrivilegeGrant.responsible_id == user_id)
		.options(
			selectinload(EventPrivilegeGrant.event),
			selectinload(EventPrivilegeGrant.promoter)
		)
	)
	return result.scalars().all()


async def get_event_grant_by_id(session: AsyncSession, grant_id: int) -> EventPrivilegeGrant | None:
	"""Возвращает привилегию по ID."""
	result = await session.get(EventPrivilegeGrant, grant_id, options=[
		selectinload(EventPrivilegeGrant.event),
		selectinload(EventPrivilegeGrant.responsible)
	])
	return result


async def get_grants_by_event(session: AsyncSession, event_id: int) -> list[EventPrivilegeGrant]:
	"""Возвращает список всех привилегий для указанного мероприятия."""
	result = await session.execute(
		select(EventPrivilegeGrant)
		.where(EventPrivilegeGrant.event_id == event_id)
		.options(
			selectinload(EventPrivilegeGrant.responsible),
			selectinload(EventPrivilegeGrant.promoter)
		)
	)
	return result.scalars().all()


async def get_active_user_event_grants(session: AsyncSession, user_id: int) -> list[EventPrivilegeGrant]:
	"""Возвращает активные привилегии пользователя на мероприятия, которые сейчас проходят."""
	now = datetime.now(timezone.utc)

	stmt = (
		select(EventPrivilegeGrant)
		.join(Event, EventPrivilegeGrant.event_id == Event.id)
		.where(
			EventPrivilegeGrant.responsible_id == user_id,
			or_(
				and_(Event.starts_at <= now, Event.ends_at > now),
				and_(Event.starts_at <= now, Event.ends_at == None)
			)
		)
		.options(
			selectinload(EventPrivilegeGrant.event),
			selectinload(EventPrivilegeGrant.promoter)
		)
	)

	result = await session.execute(stmt)
	return result.scalars().all()

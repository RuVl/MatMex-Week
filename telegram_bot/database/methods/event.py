from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.models import Event


async def create_event(
		session: AsyncSession,
		name: str,
		creator_id: int,
		visit_points: int,
		starts_at: Optional[datetime] = None,
		ends_at: Optional[datetime] = None,
		description: Optional[str] = None
) -> Event:
	"""Создаёт новое мероприятие."""
	event = Event(
		name=name,
		visit_points=visit_points,
		creator_id=creator_id,
		starts_at=starts_at,
		ends_at=ends_at,
		description=description
	)
	session.add(event)
	await session.commit()
	await session.refresh(event)
	return event


async def update_event(
		session: AsyncSession,
		event_id: int,
		name: Optional[str] = None,
		visit_points: Optional[int] = None,
		starts_at: Optional[datetime] = None,
		ends_at: Optional[datetime] = None,
		description: Optional[str] = None
) -> Event:
	"""Обновляет информацию о мероприятии."""
	event = await session.get(Event, event_id)

	if not event:
		raise ValueError(f"Мероприятие с id {event_id} не найдено")

	if name is not None:
		event.name = name

	if visit_points is not None:
		event.visit_points = visit_points

	if starts_at is not None:
		event.starts_at = starts_at

	if ends_at is not None:
		event.ends_at = ends_at

	if description is not None:
		event.description = description

	await session.commit()

	return event


async def delete_event(session: AsyncSession, event_id: int) -> bool:
	"""Удаляет мероприятие."""
	event = await session.get(Event, event_id)
	if event:
		await session.delete(event)
		await session.commit()
		return True
	return False


async def get_event_by_id(session: AsyncSession, event_id: int) -> Event | None:
	"""Возвращает мероприятие по ID."""
	return await session.get(Event, event_id, options=[
		selectinload(Event.creator),
		selectinload(Event.event_grants),
		selectinload(Event.event_attendances)
	])


async def get_all_events(session: AsyncSession) -> list[Event]:
	"""Возвращает список всех мероприятий."""
	result = await session.execute(
		select(Event)
		.order_by(Event.starts_at)
		.options(
			selectinload(Event.creator)
		)
	)
	return result.scalars().all()


async def get_upcoming_events(session: AsyncSession) -> list[Event]:
	"""Возвращает список предстоящих и текущих мероприятий (с датой начала в будущем или без даты окончания)."""
	now = datetime.now(timezone.utc)
	result = await session.execute(
		select(Event)
		.where(
			(Event.starts_at > now) |
			((Event.starts_at <= now) & (Event.ends_at > now)) |
			((Event.starts_at <= now) & (Event.ends_at == None))
		)
		.order_by(Event.starts_at)
		.options(selectinload(Event.creator))
	)
	return result.scalars().all()


async def get_events_by_creator(session: AsyncSession, creator_id: int) -> list[Event]:
	"""Возвращает список мероприятий, созданных указанным пользователем."""
	result = await session.execute(
		select(Event)
		.where(Event.creator_id == creator_id)
		.options(
			selectinload(Event.event_grants),
			selectinload(Event.event_attendances)
		)
	)
	return result.scalars().all()


async def get_active_events(session: AsyncSession) -> list[Event]:
	"""Возвращает список активных мероприятий (уже начавшихся, но еще не закончившихся)."""
	now = datetime.now(timezone.utc)
	result = await session.execute(
		select(Event)
		.where(
			((Event.starts_at - timedelta(minutes=30) <= now) & (Event.ends_at + timedelta(minutes=30) > now)) |
			((Event.starts_at - timedelta(minutes=30) <= now) & (Event.ends_at is None))
		)
		.order_by(Event.starts_at)
		.options(selectinload(Event.creator))
	)
	return result.scalars().all()

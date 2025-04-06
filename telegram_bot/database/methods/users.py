from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.models import User


async def create_user(
		session: AsyncSession,
		telegram_id: int,
		username: str,
		rights: int = 0,
		events: int = 0,
		balance: int = 0,
		promoted_by: int | None = None
) -> User:
	"""Создаёт нового пользователя с указанными параметрами."""
	user = User(
		telegram_id=telegram_id,
		username=username,
		rights=rights,
		events=events,
		balance=balance,
		promoted_by=promoted_by
	)
	session.add(user)
	await session.commit()
	return user


async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int) -> User | None:
	"""Возвращает пользователя по telegram_id с предзагрузкой связанных данных."""
	result = await session.execute(
		select(User)
			.where(User.telegram_id == telegram_id)
			.options(
			selectinload(User.promoter),
			selectinload(User.promo_codes),
			selectinload(User.activations),
			selectinload(User.purchases),
			selectinload(User.requests),
			selectinload(User.reviews)
		)
	)
	return result.scalar_one_or_none()


async def update_user_balance(session: AsyncSession, user_id: int, amount: int):
	"""Обновляет баланс пользователя."""
	await session.execute(
		update(User).where(User.id == user_id).values(balance=User.balance + amount)
	)
	await session.commit()


async def has_permission(session: AsyncSession, user_id: int, permission: int) -> bool:
	"""Проверяет, есть ли у пользователя указанное право (битовая маска)."""
	user = await session.get(User, user_id)
	return bool(user.rights & permission) if user else False


async def has_event_responsibility(session: AsyncSession, user_id: int, event_flag: int) -> bool:
	"""Проверяет, отвечает ли пользователь за указанное мероприятие (битовая маска)."""
	user = await session.get(User, user_id)
	return bool(user.events & event_flag) if user else False


async def update_user_rights(session: AsyncSession, user_id: int, rights: int):
	"""Обновляет права пользователя."""
	await session.execute(
		update(User).where(User.id == user_id).values(rights=rights)
	)
	await session.commit()


async def add_event_responsibility(session: AsyncSession, user_id: int, event_flag: int):
	"""Добавляет ответственность за мероприятие пользователю."""
	user = await session.get(User, user_id)
	if user:
		new_events = user.events | event_flag
		await session.execute(
			update(User).where(User.id == user_id).values(events=new_events)
		)
		await session.commit()


async def remove_event_responsibility(session: AsyncSession, user_id: int, event_flag: int):
	"""Удаляет ответственность за мероприятие у пользователя."""
	user = await session.get(User, user_id)
	if user:
		new_events = user.events & ~event_flag
		await session.execute(
			update(User).where(User.id == user_id).values(events=new_events)
		)
		await session.commit()


async def get_users_by_creation_date(session: AsyncSession, start_date: datetime, end_date: datetime) -> list[User]:
	"""Возвращает пользователей, созданных в указанном диапазоне дат."""
	result = await session.execute(
		select(User).where(User.created_at.between(start_date, end_date))
	)
	return result.scalars().all()


async def set_promoter(session: AsyncSession, user_id: int, promoter_id: int):
	"""Устанавливает пользователя, который дал права данному пользователю."""
	await session.execute(
		update(User).where(User.id == user_id).values(promoted_by=promoter_id)
	)
	await session.commit()

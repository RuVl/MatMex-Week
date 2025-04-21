import uuid

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.methods import get_event_by_id
from database.models import EventAttendance, User


async def create_user(session: AsyncSession, telegram_id: int, telegram_username: str, full_name: str, balance: float = 0.0) -> User:
	"""Создаёт нового пользователя с указанными параметрами."""
	user = User(telegram_id=telegram_id, telegram_username=telegram_username, full_name=full_name, balance=balance)
	session.add(user)
	await session.commit()
	await session.refresh(user)
	return user


async def user_exist_with_telegram_id(session: AsyncSession, telegram_id: int) -> bool:
	"""Есть ли пользователь в бд."""
	query = select(exists().where(User.telegram_id == telegram_id))
	result = await session.execute(query)
	return result.scalar_one()


async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int) -> User | None:
	"""Возвращает пользователя по telegram_id с предзагрузкой привилегий."""
	query = (
		select(User)
		.where(User.telegram_id == telegram_id)
		.options(
			selectinload(User.privileges),
			selectinload(User.apply),
			selectinload(User.purchases),
			selectinload(User.promocode_activations)
		)
	)
	result = await session.execute(query)
	return result.scalar_one_or_none()


async def get_user_by_code(session: AsyncSession, code: uuid.UUID) -> User | None:
	"""Возвращает пользователя по UUID-code."""
	query = (
		select(User)
		.where(User.code == code)
	)
	result = await session.execute(query)
	return result.scalar_one_or_none()


async def get_users_by_full_name(session: AsyncSession, full_name: str) -> list[User]:
	"""Возвращает пользователя по UUID-code."""
	query = (
		select(User)
		.where(User.full_name == full_name)
	)
	result = await session.execute(query)
	return result.scalars().all()


async def update_user_balance(session: AsyncSession, user_id: int, amount: float) -> User:
	"""Обновляет баланс пользователя, добавляя или вычитая сумму."""
	user = await session.get(User, user_id)
	if user:
		user.balance += amount
		await session.commit()
		await session.refresh(user)
		return user
	else:
		raise ValueError(f"Пользователь с id {user_id} не найден")


async def update_user_fullname(session: AsyncSession, user_id: int, full_name: str) -> User:
	"""Обновляет ФИО пользователя."""
	user = await session.get(User, user_id)
	if user:
		user.full_name = full_name
		await session.commit()
		await session.refresh(user)
		return user
	else:
		raise ValueError(f"Пользователь с id {user_id} не найден")


async def give_point_for_event_by_user_id(session: AsyncSession, user_id: int, event_id: int) -> bool:
	""" Отмечает определённого пользователя присутствующим на определённом мероприятии """
	event = await get_event_by_id(session, event_id)

	query = (
		select(EventAttendance)
		.where(EventAttendance.user_id == user_id, EventAttendance.event_id == event.id)
	)
	result = await session.execute(query)
	attendance = result.scalar_one_or_none()

	if attendance is not None:
		return False  # Уже посетил

	try:
		# Если пользователь еще не записан на мероприятие, то записать и отметить как посетил
		attendance = EventAttendance(user_id=user_id, event_id=event.id)
		session.add(attendance)
		await session.commit()

		await update_user_balance(session, user_id, event.visit_points)
	except Exception as e:
		await session.rollback()
		raise e

	return True

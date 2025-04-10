from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.models import User, Event, EventAttendance


async def create_user(session: AsyncSession, telegram_id: int, full_name: str, balance: float = 0.0) -> User:
	"""Создаёт нового пользователя с указанными параметрами."""
	user = User(telegram_id=telegram_id, full_name=full_name, balance=balance)
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


async def mark_user_attended_event_by_code(session: AsyncSession, user_code: str, event_id: int) -> bool:
	"""
	Отмечает, что пользователь посетил мероприятие, используя его code.

	Args:
		session: Асинхронная сессия SQLAlchemy.
		user_code: Код пользователя (uuid).
		event_id: ID мероприятия.

	Returns:
		True, если пользователь был успешно отмечен как посетивший мероприятие,
		False, если пользователь с таким кодом не найден, или если он уже был отмечен.
	"""

	try:
		# 1. Найти пользователя по code
		query = select(User).where(User.code == user_code)
		result = await session.execute(query)
		user = result.scalar_one_or_none()

		if user is None:
			print(f"User with code {user_code} not found.")
			return False

		# 2. Найти мероприятие по event_id
		event = await session.get(Event, event_id)

		if event is None:
			print(f"Event with id {event_id} not found.")
			return False

		# 3. Проверить, посетил ли пользователь уже это мероприятие
		query = select(EventAttendance).where(EventAttendance.user_id == user.id, EventAttendance.event_id == event.id)
		result = await session.execute(query)
		attendance = result.scalar_one_or_none()

		if attendance:
			if attendance.attended:
				print(f"User {user.full_name} already attended event {event.name}.")
				return False  # Уже посетил

			# Если запись о посещении есть, но attendance = False, то обновляем
			attendance.attended = True
			await session.commit()
			print(f"Updated attendance for user {user.full_name} at event {event.name}.")
			return True

		# 4. Если пользователь еще не записан на мероприятие, то записать и отметить как посетил
		attendance = EventAttendance(user_id=user.id, event_id=event.id, attended=True)
		session.add(attendance)
		await session.commit()

		print(f"User {user.full_name} marked as attended event {event.name}.")
		return True

	except Exception as e:
		print(f"Error marking user attended event: {e}")
		await session.rollback()  # Important: Rollback in case of error
		return False

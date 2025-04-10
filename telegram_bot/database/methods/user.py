from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.models import User


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

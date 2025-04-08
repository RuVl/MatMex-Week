from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User


async def create_user(session: AsyncSession, telegram_id: int, full_name: str, balance: float = 0.0) -> User:
	"""Создаёт нового пользователя с указанными параметрами."""
	user = User(telegram_id=telegram_id, full_name=full_name, balance=balance)
	session.add(user)
	await session.commit()
	await session.refresh(user)
	return user


async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int) -> User | None:
	"""Возвращает пользователя по telegram_id с предзагрузкой привилегий."""
	result = await session.execute(select(User).where(User.telegram_id == telegram_id))
	return result.scalar_one_or_none()


async def update_user_balance(session: AsyncSession, user_id: int, amount: float):
	"""Обновляет баланс пользователя, добавляя или вычитая сумму."""
	user = await session.get(User, user_id)
	if user:
		user.balance += amount
		await session.commit()
	else:
		raise ValueError(f"Пользователь с id {user_id} не найден")

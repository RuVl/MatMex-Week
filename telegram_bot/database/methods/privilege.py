from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, selectinload

from database.models import Privilege, User


async def create_privilege(session: AsyncSession, user_id: int, privilege_mask: int, provider_id: int) -> Privilege:
	"""Создаёт привилегии для пользователя с указанной битовой маской."""
	user = await session.get(User, user_id)
	if not user:
		raise ValueError(f"Пользователь с id {user_id} не найден")
	if user.privileges:
		raise ValueError("У пользователя уже есть привилегии")

	new_priv = Privilege(
		privilege=privilege_mask,
		provider_id=provider_id
	)
	session.add(new_priv)
	await session.flush()  # Получаем ID новой записи
	user.privileges_id = new_priv.id
	await session.commit()
	return new_priv


async def get_privilege_by_user(session: AsyncSession, user_id: int) -> Privilege | None:
	"""Возвращает привилегии пользователя или None, если их нет."""
	user = await session.get(User, user_id, options=[selectinload(User.privileges)])
	return user.privileges if user else None


async def has_privilege(session: AsyncSession, user_id: int, privilege_flag: int) -> bool:
	"""Проверяет, есть ли у пользователя указанная привилегия (битовая проверка)."""
	user = await session.get(User, user_id, options=[selectinload(User.privileges)])
	if user and user.privileges:
		return bool(user.privileges.privilege & privilege_flag)
	return False


async def add_privilege(session: AsyncSession, user_id: int, privilege_flag: int) -> Privilege:
	"""Добавляет привилегию к существующей битовой маске."""
	user = await session.get(User, user_id, options=[selectinload(User.privileges)])
	if not user:
		raise ValueError(f"Пользователь с id {user_id} не найден")
	if not user.privileges:
		raise ValueError(f"У пользователя с id {user_id} нет привилегий")

	user.privileges.privilege |= privilege_flag  # Добавляем флаг
	user.privileges.updated_at = datetime.now(timezone.utc)
	await session.commit()
	return user.privileges


async def remove_privilege(session: AsyncSession, user_id: int, privilege_flag: int) -> Privilege:
	"""Удаляет привилегию из битовой маски."""
	user = await session.get(User, user_id, options=[selectinload(User.privileges)])
	if not user:
		raise ValueError(f"Пользователь с id {user_id} не найден")
	if not user.privileges:
		raise ValueError(f"У пользователя с id {user_id} нет привилегий")

	user.privileges.privilege &= ~privilege_flag  # Убираем флаг
	user.privileges.updated_at = datetime.now(timezone.utc)
	await session.commit()
	return user.privileges


async def remove_all_privileges(session: AsyncSession, user_id: int):
	"""Удаляет все привилегии пользователя и каскадно убирает привилегии у тех, кому он их выдал."""
	user = await session.get(User, user_id, options=[
		selectinload(User.privileges)
	])

	if not user:
		raise ValueError(f"Пользователь с id {user_id} не найден")
	if not user.privileges:
		return  # Нечего удалять

	# Удаляем привилегии самого пользователя (остальные удалятся каскадно)
	await session.delete(user.privileges)
	user.privileges_id = None
	await session.commit()


async def get_privileges_by_provider(session: AsyncSession, provider_id: int) -> list[Privilege]:
	"""Возвращает список привилегий, выданных указанным пользователем."""
	result = await session.execute(
		select(Privilege)
		.where(Privilege.provider_id == provider_id)
		.options(selectinload(Privilege.owner))
	)
	return result.scalars().all()


async def is_provider_to(session: AsyncSession, provider_id: int, subject_id: int) -> bool:
	if provider_id == subject_id:
		return True

	privileges = Privilege.__table__

	base = select(
		privileges.c.id,
		privileges.c.provider_id
	).where(privileges.c.id == subject_id)

	recursive = base.cte(name="privilege_tree", recursive=True)
	recursive_alias = aliased(recursive)

	recursive = recursive.union_all(
		select(
			privileges.c.id,
			privileges.c.provider_id
		).where(privileges.c.id == recursive_alias.c.provider_id)
	)

	query = select(recursive.c.id).where(recursive.c.id == provider_id)
	result = await session.execute(query)

	return result.scalar() is not None

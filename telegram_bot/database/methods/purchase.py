from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.enums import ApplyStatus
from database.methods import get_item_by_id
from database.models import Purchase, User


async def get_user_purchases(session: AsyncSession, user_id: int) -> list[Purchase]:
	query = select(Purchase).where(Purchase.customer_id == user_id)
	result = await session.execute(query)
	return result.scalars().all()


async def get_purchase_by_item(session: AsyncSession, user_id: int, item_id: int) -> Purchase | None:
	query = select(Purchase).where(and_(Purchase.customer_id == user_id, Purchase.merch_id == item_id))
	result = await session.execute(query)
	return result.scalar_one_or_none()


async def add_purchase(session: AsyncSession, customer_id: int, item_id: int, price: int) -> Purchase:
	purchase = await get_purchase_by_item(session, customer_id, item_id)
	if purchase:
		purchase.quantity += 1
		purchase.total_cost += price
		await session.commit()
		return purchase
	purchase = Purchase(quantity=1, total_cost=price, customer_id=customer_id, merch_id=item_id)
	session.add(purchase)
	await session.commit()
	await session.refresh(purchase)
	return purchase


async def buy_item(session: AsyncSession, user_tg_id: int, item_id: int) -> str:
	# TODO: нужен енум по но мы до этого строками делали
	item = await get_item_by_id(session, item_id)
	query = select(User).where(User.telegram_id == user_tg_id).options(selectinload(User.apply))
	result = await session.execute(query)
	user = result.scalar_one_or_none()
	if item is None:
		return "no_such_item"
	if user is None:
		return "no_such_user"
	if not item.in_stock or item.available_count == 0:  # для безопасности
		return "item_not_in_stock"
	price = item.discount_price if user.apply and user.apply.status == ApplyStatus.APPROVED else item.full_price
	if price > user.balance:
		return "too_expensive"

	item.available_count -= 1
	user.balance -= price
	await add_purchase(session, user.id, item.id, price)
	if item.available_count == 0:
		item.in_stock = False
	await session.commit()
	return "successfully_bought"

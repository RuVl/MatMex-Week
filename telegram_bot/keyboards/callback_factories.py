from typing import Literal

from aiogram.filters.callback_data import CallbackData


class PKApplyFactory(CallbackData, prefix='apply'):
	apply_id: int
	decision: Literal['approve', 'reject', 'review']


class SupportFactory(CallbackData, prefix='support'):
	user_id: int
	message_id: int


class PrivilegeButtonFactory(CallbackData, prefix='privilege_button'):
	privilege: int
	granted: bool
	admin_id: int
	subject_id: int


class UserFactory(CallbackData, prefix='user_data'):
	full_name: str
	telegram_id: int
	telegram_username: str


class ShopCategoryFactory(CallbackData, prefix='shop_choose_category'):
	category_id: int
	can_delete: bool


class ShopDeleteCategoryFactory(CallbackData, prefix='shop_delete_category'):
	category_id: int
	can_delete: bool


class ShopItemFactory(CallbackData, prefix='shop_choose_item'):
	category_id: int
	item_id: int
	can_delete: bool


class ShopDeleteItemFactory(CallbackData, prefix='shop_delete_item'):
	category_id: int
	item_id: int
	can_delete: bool


class ShopBackToCategoriesFactory(CallbackData, prefix='back_to_categories'):
	can_delete: bool


class EditShopCategoryFactory(CallbackData, prefix='edit_shop_choose_category'):
	category_id: int


class EventFactory(CallbackData, prefix='event_button'):
	event_id: int
	can_delete: bool


class DeleteEventFactory(CallbackData, prefix='delete_event_buttton'):
	event_id: int
	can_delete: bool


class BackToEventsFactory(CallbackData, prefix='back_to_events_button'):
	can_delete: bool


class EventPrivilegeButtonFactory(CallbackData, prefix='event_privilege_button'):
	event_id: int
	grant_id: int | None
	subject_id: int


class EventToGrantFactory(CallbackData, prefix='event_to_grant_button'):
	event_id: int
	grant_id: int
	subject_id: int
	admin_tg_id: int

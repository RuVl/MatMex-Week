from aiogram.filters.callback_data import CallbackData

class SupportFactory(CallbackData, prefix='support'):
	user_id: int
	message_id: int

class ShopCategoryFactory(CallbackData, prefix='shop_choose_category'):
	category_id: int

class ShopItemFactory(CallbackData, prefix='shop_choose_item'):
	category_id: int
	item_id: int

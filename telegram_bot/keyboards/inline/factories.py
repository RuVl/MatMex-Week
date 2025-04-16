from aiogram.filters.callback_data import CallbackData

class SupportFactory(CallbackData, prefix='support'):
	user_id: int
	message_id: int
	can_delete: bool

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
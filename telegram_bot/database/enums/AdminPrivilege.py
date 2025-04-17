import enum


@enum.verify(enum.NAMED_FLAGS)

class AdminPrivilege(enum.IntFlag):
	NONE = 0
	GRANT_PRIVELEGES = 1 << 0
	EDIT_PROMOCODES = 1 << 1
	EDIT_SHOP = 1 << 2
	EDIT_EVENTS = 1 << 3
	EDIT_PK_APPLY = 1 << 4
	EDIT_MODERATORS = 1 << 5
 
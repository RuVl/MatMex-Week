import enum


@enum.verify(enum.NAMED_FLAGS)
class EventPrivilege(enum.IntFlag):
	NONE = 0
	CAN_GIVE_POINTS = 1 << 0
	TODO3 = 1 << 1
	TODO4 = 1 << 2

import enum


@enum.verify(enum.NAMED_FLAGS)
class EventPrivilege(enum.IntFlag, boundary=enum.STRICT):
	TODO1 = 0b000
	TODO2 = 0b001
	TODO3 = 0b010
	TODO4 = 0b100

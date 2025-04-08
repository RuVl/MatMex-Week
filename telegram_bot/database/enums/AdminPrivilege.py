import enum


@enum.verify(enum.NAMED_FLAGS)
class AdminPrivilege(enum.IntFlag, boundary=enum.STRICT):
	TODO1 = 0b00000
	TODO2 = 0b00001
	TODO3 = 0b00010
	TODO4 = 0b00100
	TODO5 = 0b01000
	TODO6 = 0b10000

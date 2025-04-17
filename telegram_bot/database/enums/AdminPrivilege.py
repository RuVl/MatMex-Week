import enum


@enum.verify(enum.NAMED_FLAGS)
class AdminPrivilege(enum.IntFlag, boundary=enum.STRICT):
	TODO1 = 0
	TODO2 = 1 << 0
	TODO3 = 1 << 1
	TODO4 = 1 << 2
	TODO5 = 1 << 3
	TODO6 = 1 << 4

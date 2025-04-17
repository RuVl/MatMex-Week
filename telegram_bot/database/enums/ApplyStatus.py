import enum


@enum.verify(enum.NAMED_FLAGS)
class ApplyStatus(enum.StrEnum, boundary=enum.STRICT):
	PENDING = "PENDING"
	APPROVED = "APPROVED"
	REJECTED = "REJECTED"

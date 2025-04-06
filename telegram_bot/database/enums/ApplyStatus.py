import enum


@enum.verify(enum.NAMED_FLAGS)
class ApplyStatus(enum.StrEnum, boundary=enum.STRICT):
	pending = "pending"
	approved = "approved"
	rejected = "rejected"

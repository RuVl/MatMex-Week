import enum


# Values must be in the same case
# or in model's field: Enum(ApplyStatus, values_callable=lambda obj: [e.value for e in obj])
@enum.verify(enum.NAMED_FLAGS)
class ApplyStatus(enum.StrEnum, boundary=enum.STRICT):
	PENDING = "PENDING"
	APPROVED = "APPROVED"
	REJECTED = "REJECTED"

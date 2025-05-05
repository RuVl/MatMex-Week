import enum


@enum.verify(enum.NAMED_FLAGS)
class MerchSize(enum.StrEnum, boundary=enum.STRICT):
	NONE = "NONE"
	XXS = "XXS"
	XS = "XS"
	S = "S"
	M = 'M'
	L = "L"
	XL = "XL"
	XXL = "XXL"
	XXXL = "XXXL"

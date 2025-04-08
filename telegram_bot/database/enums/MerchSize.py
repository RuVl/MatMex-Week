import enum


@enum.verify(enum.NAMED_FLAGS)
class MerchSize(enum.StrEnum, boundary=enum.STRICT):
	XXS = "XXS"
	XS = "XS"
	S = "S"
	L = "L"
	XL = "XL"
	XXL = "XXL"
	XXXL = "XXXL"

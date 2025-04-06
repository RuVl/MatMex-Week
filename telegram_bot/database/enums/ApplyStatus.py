from sqlalchemy import Enum


class ApplyStatus(Enum):
	pending = "pending"
	approved = "approved"
	rejected = "rejected"

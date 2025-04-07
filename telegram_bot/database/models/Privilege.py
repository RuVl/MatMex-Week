from datetime import datetime

from sqlalchemy import func, ForeignKey, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models import Base


class Privilege(Base):
	__tablename__ = "privileges"
	__table_args__ = {"comment": "Привилегии пользователя (o2o)"}

	id: Mapped[int] = mapped_column(primary_key=True)
	privilege: Mapped[int] = mapped_column(int, nullable=False, comment="привилегии администрирования")

	created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment="дата выдачи привилегий")
	updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False, 
												 comment="дата обновления привилегий")

	provider_id: Mapped[int] = mapped_column(ForeignKey("privileges.id"), nullable=False, comment="кем выданы")

	provider = relationship("User", backref="issued_privileges")
	user = relationship("User", back_populates="privileges", uselist=False)
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, func, String, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.models import Base


class Promocode(Base):
    __tablename__ = "promocodes"
    __table_args__ = {"comment": "Промокоды на получение баллов"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, comment="промокод (текст)")
    cost: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="количество зачисляемых баллов")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, comment="активен ли")
    max_uses: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="максимальное количество использований")
    creator_id: Mapped[int] = mapped_column(Integer, ForeignKey("privileges.id"), nullable=False, comment="кто создал")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment="когда был создан")
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, comment="когда истекает")

    activations = relationship("PromocodeActivation", back_populates="promocode")

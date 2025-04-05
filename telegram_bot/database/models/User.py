from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime

from models import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(255))
    rights = Column(Integer, default=0, nullable=False)  # Битовая маска прав
    events = Column(Integer, default=0, nullable=False)  # Битовая маска мероприятий
    balance = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    promoted_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    promoter = relationship("User", remote_side=[id], backref="promoted_users")
    promo_codes = relationship("PromoCode", back_populates="creator")
    activations = relationship("PromoActivation", back_populates="user")
    purchases = relationship("Purchase", back_populates="user")
    requests = relationship("PrivilegeRequest", back_populates="user")
    reviews = relationship("PrivilegeRequest", foreign_keys="PrivilegeRequest.reviewed_by", back_populates="reviewer")

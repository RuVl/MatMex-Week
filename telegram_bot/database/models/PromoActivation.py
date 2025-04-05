from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime

from models import Base


class PromoActivation(Base):
    __tablename__ = "promo_activations"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    promo_id = Column(Integer, ForeignKey("promo_codes.id"), nullable=False)
    activated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="activations")
    promo = relationship("PromoCode", back_populates="activations")
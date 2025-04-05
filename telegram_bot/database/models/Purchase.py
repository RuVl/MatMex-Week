from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime

from models import Base


class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    merch_id = Column(Integer, ForeignKey("merch_items.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_cost = Column(Integer, nullable=False)
    purchased_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="purchases")
    merch = relationship("MerchItem", back_populates="purchases")
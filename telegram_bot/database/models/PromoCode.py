from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from models import Base


class PromoCode(Base):
    __tablename__ = "promo_codes"
    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False)
    value = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    max_uses = Column(Integer)
    used_count = Column(Integer, default=0, nullable=False)

    creator = relationship("User", back_populates="promo_codes")
    activations = relationship("PromoActivation", back_populates="promo")

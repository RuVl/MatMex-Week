from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from models import Base


class MerchItem(Base):
    __tablename__ = "merch_items"
    id = Column(Integer, primary_key=True)
    merch_name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    stock = Column(Integer, default=0, nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)
    category_id = Column(Integer, ForeignKey("merch_categories.id"), nullable=True)

    category = relationship("MerchCategory", back_populates="items")
    purchases = relationship("Purchase", back_populates="merch")
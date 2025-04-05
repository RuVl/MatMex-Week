from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


# Таблица merch_categories
from models import Base


class MerchCategory(Base):
    __tablename__ = "merch_categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    items = relationship("MerchItem", back_populates="category")
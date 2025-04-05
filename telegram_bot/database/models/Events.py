from sqlalchemy import Column, Integer, String, DateTime

from models import Base


# Таблица events
class Events(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    date = Column(DateTime)
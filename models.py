from sqlalchemy import Column, Integer, String, Float, DateTime, func
from database import Base

class Temperature(Base):
    __tablename__ = 'temperatures'
    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)


class Pulse(Base):
    __tablename__ = 'pulses'
    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

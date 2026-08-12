from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class ParkingSpace(Base):
    __tablename__ = "parking_spaces"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(25), unique=True, Nullable=False, index=True)
    type = Column(String(25), nullable=False, default="REGULAR")
    is_active = Column(Boolean, Nullable=False, default=True)
    
    reservations = relationship("Reservation", back_populates="parking_space", cascade="all, delete-orphan")
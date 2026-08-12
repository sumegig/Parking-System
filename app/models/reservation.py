from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship
from app.database import Base

class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, index=True)
    parking_space_id = Column(Integer, ForeignKey("parking_spaces.id", ondelete="CASCADE"), nullable=False)
    applicant_name = Column(String(100), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(20), nullable=False, default="CONFIRMED")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    parking_space = relationship("ParkingSpace", back_populates="reservations")
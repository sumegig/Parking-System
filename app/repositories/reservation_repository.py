from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.reservation import Reservation

class ReservationRepository:
    def __inti__(self, db:Session):
        self.db = db
        
    def get_by_id(self, reservation_id: int) -> Optional[Reservation]:
        return self.db.query(Reservation).filter(Reservation.id == reservation_id).first()
    
    def get_by_space_id(self, parking_space_id: int, status: Optional[str] = "CONFIRMED") -> List[Reservation]:
        """Fetch all reservations for a specific parking space."""
        query = self.db.query(Reservation).filter(Reservation.parking_space_id == parking_space_id)
        if status:
            query = query.filter(Reservation.status == status)
        return query.all()
    
    def check_overlap(self, parking_space_id: int, start_time: datetime, end_time: datetime) -> Bool:
        #check for overlapping ( ExistingStart < NewEnd && ExistingEnd > NewStart)
        overlapping = (
            self.db.query(Reservation)
            .filter(
                Reservation.parking_space_id == parking_space_id,
                Reservation.status == "CONFIRMED",
                Reservation.start_time < end_time,
                Reservation.end_time > start_time,
            )
            .first()
        )
        return overlapping is not None
    
    def create(self, reservation_data: dict) -> Reservation:
        reservation = Reservation(**reservation_data)
        self.db.add(reservation)
        self.db.commit()
        self.db.refresh(reservation)
        return reservation
    
    def update_status(self, reservation_id: int, status: str) -> Optional[Reservation]:
        reservation = self.get_by_id(reservation_id)
        if reservation:
            reservation.status = status
            self.db.commit()
            self.db.refresh(reservation)
        return reservation
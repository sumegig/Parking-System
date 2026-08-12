from typing import List
from sqlalchemy.orm import Session
from app.models.reservation import Reservation
from app.repositories.parking_space_repository import ParkingSpaceRepository
from app.repositories.reservation_repository import ReservationRepository
from app.schemas.reservation import ReservationCreate

class ParkingSpaceNotFoundError(ValueError):
    pass

class ReservationConflictError(ValueError):
    pass

class ReservationService:
    def __init__(self, db: Session):
        self.db = db
        self.parking_space_repo = ParkingSpaceRepository(db)
        self.reservation_repo = ReservationRepository(db)
        
    def create_reservation(self, schema: ReservationCreate) -> Reservation:
        #checks for existing space and schedule availability before creating reservation
        
        #verify existance and status
        space = self.parking_space_repo.get_by_id(schema.parking_space_id)
        if not space or not space.is_active:
            raise ParkingSpaceNotFoundError("Parking space not found or not active")
        
        #check overlap
        has_overlap = self.reservation_repo.check_overlap(
            parking_space_id=schema.parking_space_id,
            start_time=schema.start_time,
            end_time=schema.end_time,
        )
        if has_overlap:
            raise ReservationConflictError("Reservation overlaps with existing reservation")
        
        #saev reservation
        return self.reservation_repo.create(schema.model_dump())
    
    #gets active reservations for a specific parkingspace
    def get_reservations(self, parking_space_id: int) -> List[Reservation]:
        space = self.parking_space_repo.get_by_id(parking_space_id)
        if not space:
            raise ParkingSpaceNotFoundError("Parking space not found")
        return self.reservation_repo.get_by_space_id(parking_space_id)

    def cancel_reservation(self, reservation_id: int) -> Reservation:
        reservation = self.reservation_repo.get_by_id(reservation_id)
        if not reservation:
            raise ParkingSpaceNotFoundError("Reservation not found")
        if reservation.status == "CANCELLED":
            raise ReservationConflictError("Reservation already cancelled")
        
        return self.reservation_repo.update_status(reservation_id, "CANCELLED")
    
        
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.reservation import ReservationCreate, ReservationResponse
from app.services.reservation_service import ReservationService, ReservationConflictError, ParkingSpaceNotFoundError

router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.post("", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
def create_reservation(reservation_in: ReservationCreate, db: Session = Depends(get_db)):
    service = ReservationService(db)
    try:
        return service.create_reservation(reservation_in)
    except ParkingSpaceNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ReservationConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
@router.post("/{reservation_id}/cancel", response_model=ReservationResponse, status_code=status.HTTP_200_OK)
def cancel_reservation(reservation_id: int, db: Session = Depends(get_db)):
    service = ReservationService(db)
    cancelled_reservation = service.cancel_reservation(reservation_id)
    if not cancelled_reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reservation with ID {reservation_id} not found or already cancelled")
    return cancelled_reservation
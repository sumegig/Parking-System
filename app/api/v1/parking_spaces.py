from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.parking_space import ParkingSpaceResponse
from app.schemas.reservation import ReservationResponse
from app.repositories.parking_space_repository import ParkingSpaceRepository
from app.repositories.reservation_repository import ReservationRepository

router = APIRouter(prefix="/parking-spaces", tags=["Parking Spaces"])

@router.get("", response_model=List[ParkingSpaceResponse], status_code=status.HTTP_200_OK)
def get_parking_spaces(db: Session = Depends(get_db)):
    #get all available parking spaces
    repo = ParkingSpaceRepository(db)
    return repo.get_all_active()

@router.get("/{space_id}/reservations", response_model=List[ReservationResponse], status_code=status.HTTP_200_OK)
def get_reservations(space_id: int, 
                     start_time: Optional[datetime] = Query(None, description="Start time of the reservation"),
                     end_time: Optional[datetime] = Query(None, description="End time of the reservation"),
                     db: Session = Depends(get_db)):
    #get all reservatuons for a parking space
    space_repo = ParkingSpaceRepository(db)
    if not space_repo.get_by_id(space_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parking space with ID {space_id} not found")
    
    reservation_repo = ReservationRepository(db)
    return reservation_repo.get_by_space_id(space_id = space_id, start_time = start_time, end_time = end_time)
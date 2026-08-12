from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.parking_space import ParkingSpace

class ParkingSpaceRepository:
    def __init__(self, db: Session):
        self.db = db
        
        #single parking space by primary ID
    def get_by_id(self, space_id:int) -> Optional[ParkingSpace]:
        return self.db.query(ParkingSpace).filter(ParkingSpace.id == space_id).first()
    
        #single parking space by code
    def get_by_code(self, space_code: str) -> Optional[ParkingSpace]:
        return self.db.query(ParkingSpace).filter(ParkingSpace.code == space_code).first()
    
    def get_all_active(self) -> List[ParkingSpace]:
        return self.db.query(ParkingSpace).filter(ParkingSpace.is_active == True).all()
    
    def get_all(self) -> List[ParkingSpace]:
        return self.db.query(ParkingSpace).all()
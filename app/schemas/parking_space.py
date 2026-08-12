from pydantic import BaseModel

class ParkingSpaceBase(BaseModel):
    code: str
    type: str = "REGULAR"
    is_active: bool = True
    
class ParkingSpaceCreate(ParkingSpaceBase):
    pass

class ParkingSpace(ParkingSpaceBase):
    id: int
    
    class Config:
        from_attributes = True

class ParkingSpaceResponse(ParkingSpace):
    pass
from pydantic import BaseModel, ConfigDict

class ParkingSpaceBase(BaseModel):
    code: str
    type: str = "REGULAR"
    is_active: bool = True
    
class ParkingSpaceCreate(ParkingSpaceBase):
    pass

class ParkingSpace(ParkingSpaceBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class ParkingSpaceResponse(ParkingSpace):
    pass
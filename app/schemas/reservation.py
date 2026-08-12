from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, model_validator

class ReservationBase(BaseModel):
    parking_space_id: int
    applicant_name: str = Field(..., min_length=2, max_length=100)
    start_time: datetime
    end_time: datetime
    
class ReservationCreate(ReservationBase):
    @model_validator(mode="after")
    def validate_times(self) -> "ReservationCreate":
        if self.start_time >= self.end_time:
            raise ValueError("Start time must be before end time")
        return self
    
class ReservationResponse(ReservationBase):
    id: int
    status: str 
    created_at: datetime
    
    class Config:
        from_attributes = True
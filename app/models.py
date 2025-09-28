from datetime import datetime, timezone
from pydantic import BaseModel, Field, validator
from typing import Optional

class MessageIn(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    content: str = Field(..., min_length=1, max_length=1000)

class Message(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    room: str
    username: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc).isoformat()
        }

    @validator("id", pre=True, always=True)
    def convert_id(cls, v):
        return str(v) if v else None

class MessageOut(BaseModel):
    id: str = Field(..., alias="_id")
    room: str
    username: str
    content: str
    created_at: str

    class Config:
        allow_population_by_field_name = True

    @validator("id", pre=True, always=True)
    def convert_id(cls, v):
        return str(v)

    @validator("created_at", pre=True, always=True)
    def convert_created_at(cls, v):
        if isinstance(v, datetime):
            return v.replace(tzinfo=timezone.utc).isoformat()
        return v


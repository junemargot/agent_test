from pydantic import BaseModel, Field
from typing import List, Optional, Tuple
from datetime import datetime

class MealServiceCreate(BaseModel):
    name: str
    address: str
    coordinates: Tuple[float, float]
    phone: Optional[str] = None
    operating_hours: Optional[str] = None
    target_audience: Optional[str] = None
    services: Optional[List[str]] = None

class MealServiceResponse(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    address: str
    location: dict
    phone: Optional[str] = None
    operating_hours: Optional[str] = None
    target_audience: Optional[str] = None
    services: Optional[List[str]] = None
    updated_at: datetime

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "name": "행복한 무료급식소",
                "address": "서울시 강남구 테헤란로 123",
                "location": {"type": "Point", "coordinates": [127.036553, 37.495506]},
                "phone": "02-123-4567",
                "operating_hours": "평일 11:30-13:00",
                "target_audience": "만 65세 이상 노인",
                "services": ["중식", "석식", "도시락 배달"],
                "updated_at": "2023-04-20T10:30:00Z"
            }
        }

class NearbyQueryParams(BaseModel):
    longitude: float
    latitude: float
    max_distance: int = 3000  # 미터 단위, 기본값 3km
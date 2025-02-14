from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class MealServiceModel(BaseModel):
  """MongoDB 문서 구조를 정의합니다."""
  name: str
  address: str
  location: dict = Field(..., example={"type": "Point", "coordinates": [127.0, 37.5]})
  phone: Optional[str] = None
  operating_hours: Optional[str] = None
  target_audience: Optional[str] = None
  services: Optional[List[str]] = None
  updated_at: datetime = Field(default_factory=datetime.now)
  
  class Config:
      schema_extra = {
          "example": {
              "name": "행복한 무료급식소",
              "address": "서울시 강남구 테헤란로 123",
              "location": {"type": "Point", "coordinates": [127.036553, 37.495506]},
              "phone": "02-123-4567",
              "operating_hours": "평일 11:30-13:00",
              "target_audience": "만 65세 이상 노인",
              "services": ["중식", "석식", "도시락 배달"]
          }
      }
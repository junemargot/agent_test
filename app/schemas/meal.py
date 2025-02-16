from pydantic import BaseModel

class MealRequest(BaseModel):
  user_query: str
  location: str | None = None

class MealResponse(BaseModel):
  result: list[dict]
  metadata: dict
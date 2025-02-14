from fastapi import APIRouter, Request, HTTPException, Depends
from typing import List
from bson import ObjectId
from app.schemas.meal_service import MealServiceCreate, MealServiceResponse, NearbyQueryParams
from app.models.meal_service import MealServiceModel
from app.ai.agent import AIAgent

router = APIRouter()

# 위도/경도 기준 주변 급식소 조회
@router.get("/nearby", response_model=List[MealServiceResponse])
async def get_nearby_meal_services(
    request: Request,
    params: NearbyQueryParams = Depends()
):
    query = {
        "location": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [params.longitude, params.latitude]
                },
                "$maxDistance": params.max_distance
            }
        }
    }
    
    cursor = request.app.mongodb["meal_services"].find(query)
    services = await cursor.to_list(length=50)
    
    for service in services:
        service["_id"] = str(service["_id"])
    
    return services

# 모든 급식소 조회 
@router.get("/", response_model=List[MealServiceResponse])
async def get_all_meal_services(request: Request, skip: int = 0, limit: int = 100):
    cursor = request.app.mongodb["meal_services"].find().skip(skip).limit(limit)
    services = await cursor.to_list(length=limit)
    
    for service in services:
        service["_id"] = str(service["_id"])
    
    return services

# 상세 정보 조회
@router.get("/{id}", response_model=MealServiceResponse)
async def get_meal_service(id: str, request: Request):
    if (service := await request.app.mongodb["meal_services"].find_one({"_id": ObjectId(id)})) is not None:
        service["_id"] = str(service["_id"])
        return service
    raise HTTPException(status_code=404, detail=f"급식소를 찾을 수 없습니다: {id}")

ai_agent = AIAgent()

@router.post("/query")
async def process_query(
    request: Request,
    query: str,
    longitude: float = None,
    latitude: float = None
):
    
    user_location = [longitude, latitude] if longitude is not None and latitude is not None else None
    response = await ai_agent.process_user_query(request, query, user_location)
    return response
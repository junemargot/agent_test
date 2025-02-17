from fastapi import APIRouter, HTTPException, Body
from app.llm.agent import MealAgent
from app.services.data_client import PublicDataClient
from pydantic import BaseModel

# POST 요청의 body를 위한 Pydantic 모델
class QueryRequest(BaseModel):
  query: str

# FastAPI 라우터 및 클래스 인스턴스 생성
router = APIRouter() 
data_client = PublicDataClient()
meal_agent = MealAgent(data_client=data_client)

# AI 기반 무료급식소 검색 엔드포인트
@router.post("/meal-agent")
async def handle_meal_query(request: QueryRequest):
  try:
    print(f"DEBUG: 요청 쿼리: {request.query}")
    response = meal_agent.generate_response(request.query)

    print(f"DEBUG: 생성된 응답: {response}")
    return {"answer": response}
  
  except Exception as e:
    print(f"DEBUG: Error occurred: {str(e)}")
    raise HTTPException(500, detail=str(e))
  
# 무료급식소 데이터 확인 엔드포인트
@router.get("/debug-meal-services")
async def debug_meal_services():
  """무료급식소 데이터 전체 조회 (디버깅용)"""
  data = data_client.fetch_meal_services()
  return {"data": data}

# 특정 지역 무료급식소 필터링 엔드포인트
@router.get("/debug-filter")
async def debug_filter(region: str):
    """특정 지역의 무료급식소 반환 (디버깅용)"""
    raw_data = data_client.fetch_meal_services()
    filtered_data = data_client.filter_by_region(raw_data, region)
    return {"filtered_data": filtered_data}

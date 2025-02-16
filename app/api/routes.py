from fastapi import APIRouter, HTTPException
from app.llm.agent import MealAgent
from app.services.data_client import PublicDataClient

router = APIRouter()
agent = MealAgent()
data_client = PublicDataClient()

@router.get("/meal-services")
async def get_meal_services(page: int = 1, size: int = 50):
    try:
        return data_client.fetch_meal_services(page, size)
    except Exception as e:
        raise HTTPException(500, detail=str(e))

@router.post("/meal-agent")
async def handle_meal_query(query: str):
    try:
        return {"answer": await agent.generate_response(query)}
    except Exception as e:
        raise HTTPException(500, detail=str(e))
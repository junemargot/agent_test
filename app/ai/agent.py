from fastapi import Request
from typing import List, Dict, Any

class AIAgent:
    def __init__(self):
        # 초기화 로직 (필요 시 ML 모델 로드)
        pass
    
    async def get_recommendations(
        self, 
        request: Request,
        user_location: tuple,
        user_preferences: Dict[str, Any] = None
    ) -> Dict[str, List[Dict]]:
        """사용자 위치와 선호도를 기반으로 추천을 제공합니다."""
        db = request.app.mongodb
        
        # 주변 급식소 찾기
        meal_query = {
            "location": {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": user_location
                    },
                    "$maxDistance": 2000  # 2km 이내
                }
            }
        }
        
        meal_cursor = db["meal_services"].find(meal_query).limit(5)
        meal_services = await meal_cursor.to_list(length=5)
        
        # 주변 직업소개소 찾기
        job_query = {
            "location": {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": user_location
                    },
                    "$maxDistance": 2000  # 2km 이내
                }
            }
        }
        
        job_cursor = db["job_services"].find(job_query).limit(5)
        job_services = await job_cursor.to_list(length=5)
        
        # ID를 문자열로 변환
        for service in meal_services + job_services:
            service["_id"] = str(service["_id"])
        
        return {
            "meal_services": meal_services,
            "job_services": job_services
        }
    
    async def process_user_query(
        self,
        request: Request,
        query: str,
        user_location: tuple = None
    ) -> Dict[str, Any]:
        """사용자 자연어 쿼리를 처리하고 적절한 응답을 반환합니다."""
        # 실제 구현에서는 NLP 모델을 사용하여 의도 파악
        # 간단한 예시로 키워드 기반 로직 구현
        
        response = {
            "type": "text",
            "content": "어떻게 도와드릴까요?",
            "recommendations": []
        }
        
        if "급식" in query or "식사" in query or "밥" in query:
            if user_location:
                meal_query = {
                    "location": {
                        "$near": {
                            "$geometry": {
                                "type": "Point",
                                "coordinates": user_location
                            },
                            "$maxDistance": 3000
                        }
                    }
                }
                meal_cursor = request.app.mongodb["meal_services"].find(meal_query).limit(3)
                recommendations = await meal_cursor.to_list(length=3)
                
                for service in recommendations:
                    service["_id"] = str(service["_id"])
                
                response = {
                    "type": "recommendation",
                    "content": "주변에 있는 무료급식소입니다:",
                    "recommendations": recommendations
                }
            else:
                response["content"] = "주변 급식소를 찾으려면 위치 정보가 필요합니다."
        
        elif "일자리" in query or "직업" in query or "취업" in query:
            if user_location:
                job_query = {
                    "location": {
                        "$near": {
                            "$geometry": {
                                "type": "Point",
                                "coordinates": user_location
                            },
                            "$maxDistance": 3000
                        }
                    }
                }
                job_cursor = request.app.mongodb["job_services"].find(job_query).limit(3)
                recommendations = await job_cursor.to_list(length=3)
                
                for service in recommendations:
                    service["_id"] = str(service["_id"])
                
                response = {
                    "type": "recommendation",
                    "content": "주변에 있는 무료직업소개소입니다:",
                    "recommendations": recommendations
                }
            else:
                response["content"] = "주변 직업소개소를 찾으려면 위치 정보가 필요합니다."
        
        return response
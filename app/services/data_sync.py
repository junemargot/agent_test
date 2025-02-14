import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from app.config import settings
from motor.motor_asyncio import AsyncIOMotorClient

async def sync_meal_services():
    """전국무료급식소 데이터를 동기화"""
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    collection = db["meal_services"]
    
    # 공공데이터 API 호출 (실제 API URL로 대체 필요)
    url = "http://api.data.go.kr/openapi/tn_pubr_public_free_mlsv_api"
    params ={'serviceKey' : '서비스키', 'pageNo' : '1', 'numOfRows' : '100', 'type' : 'xml', 'fcltyNm' : '', 'rdnmadr' : '', 'lnmadr' : '', 'operInstitutionNm' : '', 'phoneNumber' : '', 'mlsvPlace' : '', 'mlsvTrget' : '', 'mlsvTime' : '', 'mlsvDate' : '', 'operOpenDate' : '', 'operCloseDate' : '', 'latitude' : '', 'longitude' : '', 'referenceDate' : '', 'instt_code' : '' }

    response = requests.get(url, params=params)
    print(response.content)
    
    if response.status_code != 200:
        print(f"API 호출 실패: {response.status_code}")
        return
    
    # XML 파싱 예시 (실제 응답 형식에 맞게 조정 필요)
    root = ET.fromstring(response.content)
    for item in root.findall(".//item"):
        # 데이터 추출 및 가공
        name = item.find("name").text
        address = item.find("address").text
        # 좌표 변환 (예시)
        lat = float(item.find("latitude").text)
        lng = float(item.find("longitude").text)
        
        # MongoDB 문서 생성/업데이트
        service_data = {
            "name": name,
            "address": address,
            "location": {
                "type": "Point",
                "coordinates": [lng, lat]
            },
            "phone": item.find("phone").text if item.find("phone") is not None else None,
            "operating_hours": item.find("operatingHours").text if item.find("operatingHours") is not None else None,
            "target_audience": item.find("targetAudience").text if item.find("targetAudience") is not None else None,
            "services": [s.strip() for s in item.find("services").text.split(",")] if item.find("services") is not None else None,
            "updated_at": datetime.now()
        }
        
        # 업데이트 또는 삽입
        await collection.update_one(
            {"name": name, "address": address},
            {"$set": service_data},
            upsert=True
        )
    
    client.close()
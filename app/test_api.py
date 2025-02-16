import os
import requests
import json
import urllib.parse
import pandas as pd
import xml.etree.ElementTree as ET

from dotenv import load_dotenv
load_dotenv(override=True)
# load_dotenv()

# API 키 가져오기
DATA_API_KEY = os.getenv("DATA_DECODING_KEY")

# API 호출 테스트
def test_meal_services():
  """무료급식소 api 테스트"""
  serviceKey = DATA_API_KEY
  url = f"http://api.data.go.kr/openapi/tn_pubr_public_free_mlsv_api?serviceKey={serviceKey}&pageNo=1&numOfRows=50&type=json"
  print(f"API 요청 URL: {url}")
  print(f"서비스키: {serviceKey}")
  params = {
    "serviceKey": serviceKey,  # 필수 API 인증 키
    "type": "json",            # JSON 형식으로 응답 받기 (따옴표 명확히 감싸기)
    "pageNo": 1,               # 페이지 번호
    "numOfRows": 50,           # 가져올 데이터 개수
    "fcltyNm": "",             # 
    "rdnmadr": ""
  }

  # response = requests.get(url, params=params)
  response = requests.get(url)
  print(f"상태 코드: {response.status_code}")
  # print(f"응답 결과: {response.content}")
  
  if response.status_code != 200:
    return {"error": "API 호출 실패", "status_code": response.status_code}
  
  # JSON 응답 파싱
  json_data = response.json()

  # 응답결과 코드 확인
  result_code = json_data['response']['header']['resultCode']
  if result_code != "00":
    print(f"에러 발생: {json_data['response']['header']['resultMsg']}")
    return
  
  # items 키 존재하는 확인
  if 'items' in json_data['response']['body']:
    items = json_data['response']['body']['items']
    print(f"항목 수: {len(items)}")

    for item in items:
      fcltyNm = item['fcltyNm']
      rdnmadr = item['rdnmadr']
      print(f"시설명: {fcltyNm}")
      print(f"주소: {rdnmadr}")

  else:
    print("응답 데이터에 'items' 키가 없습니다.")

  
if __name__ == "__main__":
  print("무료급식소 API 테스트 시작")
  test_meal_services()

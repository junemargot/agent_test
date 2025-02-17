import requests
from app.core.config import settings

class PublicDataClient:
  def __init__(self):
    """
    PublicDataClient 클래스: 공공데이터 API를 통해 무료급식소 정보 가져오기
    """
    self.base_url = "http://api.data.go.kr/openapi/tn_pubr_public_free_mlsv_api"
    self.service_key = settings.DATA_DECODING_KEY

  def fetch_meal_services(self, page: int=1, num_of_rows: int=1500):
    """
    전국무료급식소표준데이터를 API에서 불러온 후, 필드명을 매핑하여 반환한다.
    :param page: 가져올 페이지 번호 (기본값 1)
    :param num_of_rows: 한 번에 가져올 데이터 개수(기본값 1500)
    '시설명', '소재지도로명주소' 등 한국어 필드명을
    'fcltyNm', 'rdnmadr' 등 영문 키로 매핑하여 반환합니다.
    """

    # 1. API 호출을 위한 요청 파라미터 설정
    params = {
      "serviceKey": self.service_key, # API 인증키
      "pageNo": page,                 # 페이지 번호
      "numOfRows": num_of_rows,       # 한 페이지당 데이터 개수
      "type": "json"                  # 응답 형식(JSON)
    }

    # 2. API 호출(GET 요청)
    response = requests.get(self.base_url, params=params)
    response.raise_for_status() # 요청 실패 시 예외 발생(HTTP 오류 시 중단)
    
    json_data = response.json() # 응답 데이터를 JSON 형식으로 파싱
    
    print("DEBUG: API Response:", json_data) # 디버깅을 위한 응답 데이터 출력
    
    # 3. API 응답 오류 처리
    if json_data['response']['header']['resultCode'] != "00":
      # API에서 오류 코드가 반환되면 예외 발생
      raise ValueError(f"API Error: {json_data['response']['header']['resultMsg']}")
    
    # 4. 응답에서 필요한 데이터 부분 추출
    items = json_data['response']['body']['items']
    # 'items'에 무료급식소 데이터가 담긴 딕셔너리인 경우 처리
    if isinstance(items, dict): 
        items = items.get('item', [])
    
    if not items:  # 데이터가 없을 경우, 빈 리스트 반환
        print("DEBUG: No items found in response")
        return []
    
    # 5. API 응답 필드를 표준화하여 변환 (필드명 매핑)
    normalized_records = []
    for item in items:
        # 디버깅을 위한 개별 아이템 출력
        print("DEBUG: Processing item:", item)
        
        normalized = {
            "fcltyNm":  item.get("fcltyNm", ""),                      # 시설명
            "rdnmadr":  item.get("rdnmadr", ""),                      # 도로명주소
            "lnmadr":   item.get("lnmadr", ""),                       # 지번주소
            "operInstitutionNm": item.get("operInstitutionNm", ""),   # 운영기관명
            "phoneNumber":       item.get("phoneNumber", ""),         # 전화번호
            "mlsvPlace":         item.get("mlsvPlace", ""),           # 급식장소   
            "mlsvTrget":         item.get("mlsvTrget", ""),           # 급식대상 
            "mlsvTime":          item.get("mlsvTime", ""),            # 급식시간
            "mlsvDate":          item.get("mlsvDate", "")             # 급식일자
        }
        normalized_records.append(normalized)  # 변환된 데이터를 리스트에 추가
    
    return normalized_records  # 정리된 데이터 리스트 반환

  def filter_by_region(self, data: list, region: str) -> list:
    """
    지역(region) 정보가 포함된 급식소 데이터를 필터링한다.

    :param data: 필터링할 데이터 리스트
    :param region: 필터링할 지역명(예: "성동구", "강남구")
    :return: 필터링된 무료급식소 데이터 리스트
    """

    # 데이터 리스트에서 'rdnmadr'(도로명주소)에 지역명이 포함된 항목만 추출
    filtered_data = [
      item for item in data
      if region in item.get("rdnmadr", "")
    ]

    return filtered_data  # 필터링된 데이터 리스트 반환
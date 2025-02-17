from openai import OpenAI
from cachetools import TTLCache
from app.core.config import settings
from app.services.data_client import PublicDataClient

client = OpenAI(api_key=settings.OPENAI_API_KEY)

class MealAgent: 
  """
  무료급식소 정보를 제공하는 AI 기반 에이전트.
  사용자 질문을 분석하여 지역 정보를 추출하고, 필터링된 급식소 데이터를 반환합니다.
  """
  def __init__(self, data_client: PublicDataClient):
    self.data_client = data_client # 공공데이터 API에서 데이터를 가져오는 객체
    self.cache = TTLCache(maxsize=100, ttl=300) # 최대 100개 저장, 5분간 유지
    self.SYSTEM_PROMPT = """
      당신은 고령층을 위한 무료 급식소 안내 전문가입니다.
      사용자가 요청한 지역(예: {region})에 해당하는 무료급식소 정보를 아래 데이터에서 찾아주세요.
      - 65세 이상 대상자 우선 제공
      - 주소 설명시 주변 지점 설명
      - 자세한 급식소 안내를 위해 사용자가 이용하고자하는 지역을 추출할 것
      - 이모티콘을 붙여 친근하고, 존댓말을 사용할 것

      데이터 형식:
      - 시설명: {fcltyNm}
      - 주소: {rdnmadr}

      질문: {query}
      """
  
  def generate_response(self, query: str) -> str:
    """
    사용자의 질문에 대해 무료급식소 정보를 제공하는 응답을 생성합니다.
    
    Args:
      query (str): 사용자의 질문 (예: "성동구 무료급식소")
        
    Returns:
      str: 질문에 대한 응답
    """
    print(f"DEBUG: 사용자 입력 query: '{query}'")
    
    # 1. 지역명 추출 (예: "성동구")
    region = self._extract_region(query)
    print(f"DEBUG: 결과 - Extracted region: '{region}'")  # 추출된 지역명 출력
    
    if not region:
      return "죄송합니다. 어느 지역의 무료 급식소를 찾으시는지 명확히 말씀해 주시겠어요?"

    # 2. 데이터 가져오기
    all_data = self.data_client.fetch_meal_services()
    print(f"DEBUG: 결과 - 사용자 요청 지역: {region}")      # 지역명 출력

    # 3. 지역 기반 필터링
    filtered_data = self.data_client.filter_by_region(all_data, region)
    print(f"DEBUG: 결과 - 필터된 데이터: {filtered_data}")  # 필터링된 데이터 출력  
    
    # 4. AI 응답 생성
    if not filtered_data:
      return f"죄송합니다. 현재 {region}의 무료 급식소 정보를 찾을 수 없습니다. 🙏\n다른 지역을 검색해보시겠어요? (예: 서대문구, 중구 등)"
    
    response = f"{region}에서 {len(filtered_data)}개의 무료 급식소를 찾았습니다:\n\n"
    
    for item in filtered_data:
      response += f"- {item['fcltyNm']}\n"
      response += f"  주소: {item['rdnmadr']}\n"
      response += f"  운영: {item['operInstitutionNm']}\n"
      response += f"  급식시간: {item['mlsvTime']}\n"
      response += f"  급식대상: {item['mlsvTrget']}\n\n"
    
    return response

  def _extract_region(self, query: str) -> str:
    """
    질문에서 지역명을 추출합니다.
    
    Args:
      query (str): 사용자의 질문
        
    Returns:
      str: 추출된 지역명 또는 빈 문자열
    """
    
    words = query.split()
    for word in words:
      # "구"가 포함된 단어에서 조사 제거
      if "구" in word:
        # "구"로 끝나는 경우 그대로 반환
        if word.endswith("구"):
            return word
        # "구" 다음에 다른 문자가 있는 경우 (예: "구에", "구는" 등)
        # "구" 위치까지만 잘라서 반환
        idx = word.index("구")
        return word[:idx+1]
    return ""
import requests
from app.core.config import settings

class PublicDataClient:
  def __init__(self):
    self.base_url = "http://api.data.go.kr/openapi/tn_pubr_public_free_mlsv_api"
    self.service_key = settings.DATA_DECODING_KEY

  def fetch_meal_services(self, page: int = 1, num_of_rows: int = 50) -> list:
    params = {
      "serviceKey": self.service_key,
      "pageNo": page,
      "numOfRows": num_of_rows,
      "type": "json"
    }
      
    response = requests.get(self.base_url, params=params)
    response.raise_for_status()
    
    json_data = response.json()
    if json_data['response']['header']['resultCode'] != "00":
      raise ValueError(f"API Error: {json_data['response']['header']['resultMsg']}")
        
    return json_data['response']['body']['items']

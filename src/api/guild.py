import requests

from config import API_KEY, GUILD_BASIC_URL, GUILD_ID_URL
from src.utils import global_rate_limit


@global_rate_limit
def get_guild_id(guild_name, world_name):
    """길드 이름과 월드를 받아 oguild_id 조회"""
    headers = {"accept": "application/json", "x-nxopen-api-key": API_KEY}
    params = {"guild_name": guild_name, "world_name": world_name}
    response = requests.get(GUILD_ID_URL, headers=headers, params=params)
    # 강제로 UTF-8 인코딩 설정
    response.encoding = "utf-8"
    if response.status_code == 200:
        try:
            data = response.json()
            return data.get("oguild_id")
        except ValueError:
            raise Exception(f"Guild ID API 응답이 JSON 형식이 아님: {response.text}")
    else:
        raise Exception(f"Guild ID API 호출 실패: {response.status_code} {response.text}")


@global_rate_limit
def get_guild_basic(oguild_id, date):
    """oguild_id와 조회 날짜(어제 날짜)를 받아 길드 기본 정보 조회"""
    headers = {"accept": "application/json", "x-nxopen-api-key": API_KEY}
    params = {"oguild_id": oguild_id, "date": date}
    response = requests.get(GUILD_BASIC_URL, headers=headers, params=params)
    response.encoding = "utf-8"
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            raise Exception(f"Guild Basic API 응답이 JSON 형식이 아님: {response.text}")
    else:
        raise Exception(f"Guild Basic API 호출 실패: {response.status_code} {response.text}")

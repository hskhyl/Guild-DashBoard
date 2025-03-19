import requests

from config import API_KEY, CHARACTER_BASIC_URL, CHARACTER_FINAL_STAT_URL, CHARACTER_ID_URL, CHARACTER_UNION_INFO_URL
from src.utils import global_rate_limit


def fetch_api(url, params):
    """공통 API 요청 함수"""
    headers = {"accept": "application/json", "x-nxopen-api-key": API_KEY}
    response = requests.get(url, headers=headers, params=params)
    # 강제로 UTF-8 인코딩 설정
    response.encoding = "utf-8"
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            raise Exception(f"API 응답이 JSON 형식이 아님: {url} -> {response.text}")
    else:
        raise Exception(f"API 호출 실패 ({url}): {response.status_code} {response.text}")


@global_rate_limit
def get_character_ocid(character_name):
    """캐릭터 이름을 받아 ocid 조회"""
    params = {"character_name": character_name}
    data = fetch_api(CHARACTER_ID_URL, params)
    return data.get("ocid")


@global_rate_limit
def get_character_basic(ocid, date):
    """ocid와 조회 날짜를 받아 캐릭터 기본 정보 조회"""
    params = {"ocid": ocid, "date": date}
    return fetch_api(CHARACTER_BASIC_URL, params)


@global_rate_limit
def get_character_stat(ocid, date):
    """캐릭터 최소 스탯 공격력 조회"""
    params = {"ocid": ocid, "date": date}
    data = fetch_api(CHARACTER_FINAL_STAT_URL, params)
    return float(data["final_stat"][0]["stat_value"])


@global_rate_limit
def get_union_info(ocid, date):
    """유니온 정보 조회"""
    params = {"ocid": ocid, "date": date}
    data = fetch_api(CHARACTER_UNION_INFO_URL, params)
    return data.get("union_level")

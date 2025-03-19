# src/api/character.py

import requests

from config import API_KEY, CHARACTER_BASIC_URL, CHARACTER_ID_URL
from src.utils import global_rate_limit


@global_rate_limit
def get_character_ocid(character_name):
    """캐릭터 이름을 받아 ocid 조회"""
    headers = {"accept": "application/json", "x-nxopen-api-key": API_KEY}
    params = {"character_name": character_name}
    response = requests.get(CHARACTER_ID_URL, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("ocid")
    else:
        raise Exception(f"Character ID API 호출 실패 ({character_name}): {response.status_code} {response.text}")


@global_rate_limit
def get_character_basic(ocid, date):
    """ocid와 조회 날짜(어제 날짜)를 받아 캐릭터 기본 정보 조회"""
    headers = {"accept": "application/json", "x-nxopen-api-key": API_KEY}
    params = {"ocid": ocid, "date": date}
    response = requests.get(CHARACTER_BASIC_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Character Basic API 호출 실패 (ocid: {ocid}): {response.status_code} {response.text}")

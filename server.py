# server.py
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse

from src.api import character as character_api
from src.api import guild as guild_api
from src.stats.aggregator import aggregate_guild_stats
from src.utils import get_previous_date


app = FastAPI(title="Maplestory Guild Dashboard API")


@app.get(
    "/guild",
    summary="길드 정보 및 집계 결과 조회",
    description="길드 이름과 월드명을 기반으로 길드 정보 및 구성원 집계 결과를 반환합니다.",
)
def get_guild_dashboard(
    guild_name: str = Query(..., description="길드 이름"), world_name: str = Query(..., description="월드 이름")
):
    """
    1. 어제 날짜를 기준으로 길드 ID와 기본 정보를 조회
    2. 길드원 각각의 개인 식별자(ocid) 및 기본 정보를 조회
    3. 조회된 길드원 정보를 집계하여 통계(평균 레벨, 클래스 분포, 성별 분포 등)를 계산
    4. 길드 기본 정보, 집계 결과, 에러 정보를 JSON 형태로 반환
    """
    previous_date = get_previous_date()

    try:
        # 1. 길드 ID 및 기본 정보 조회
        oguild_id = guild_api.get_guild_id(guild_name, world_name)
        guild_info = guild_api.get_guild_basic(oguild_id, previous_date)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"길드 정보 조회 실패: {e}")

    # 2. 각 길드원 개별 정보 조회
    members = guild_info.get("guild_member", [])
    character_info_list = []
    errors = {}  # 각 길드원별 에러 기록
    for member_name in members:
        try:
            ocid = character_api.get_character_ocid(member_name)
            char_info = character_api.get_character_basic(ocid, previous_date)
            character_info_list.append(char_info)
        except Exception as e:
            errors[member_name] = str(e)

    # 3. 통계 집계 (예: 평균 레벨, 클래스 분포, 성별 분포 등)
    stats = aggregate_guild_stats(character_info_list)

    # 4. 결과 반환
    result = {"guild_info": guild_info, "aggregated_stats": stats, "errors": errors}
    return JSONResponse(content=result)

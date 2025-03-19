from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

from src.api import character as character_api
from src.api import guild as guild_api
from src.stats.aggregator import aggregate_guild_stats
from src.utils import get_previous_date


# 로깅 설정
logger.add("guild_dashboard.log", rotation="10 MB", level="INFO", encoding="utf-8-sig")

app = FastAPI(title="Maplestory Guild Dashboard API")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Guild Dashboard API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get(
    "/guild",
    summary="길드 정보 및 집계 결과 조회",
    description="길드 이름과 월드명을 기반으로 길드 정보 및 구성원 집계 결과를 반환합니다.",
)
def get_guild_dashboard(
    guild_name: str = Query(None, description="길드 이름"),
    world_name: str = Query(None, description="월드 이름"),
    previous_date: str = Depends(get_previous_date),
):
    if not guild_name or not world_name:
        raise HTTPException(status_code=400, detail="길드 이름과 월드명을 입력해야 합니다.")

    logger.info(
        f"길드 조회 요청: {guild_name.encode('utf-8', 'ignore').decode('utf-8')} ({world_name.encode('utf-8', 'ignore').decode('utf-8')}), 기준 날짜: {previous_date}"
    )

    try:
        # 1. 길드 기본 정보 조회
        oguild_id = guild_api.get_guild_id(guild_name, world_name)
        guild_info = guild_api.get_guild_basic(oguild_id, previous_date)
        logger.info(f"길드 정보 조회 성공: {guild_name} (ID: {oguild_id})")
    except Exception as e:
        logger.error(f"길드 정보 조회 실패: {e}")
        raise HTTPException(status_code=400, detail=f"길드 정보 조회 실패: {e}")

    # 2. 길드원 정보 조회
    members = guild_info.get("guild_member", [])
    if not members:
        logger.warning(f"길드에 등록된 길드원이 없습니다: {guild_name}")
        return JSONResponse(content={"guild_info": guild_info, "aggregated_stats": {}, "errors": {}})

    character_info_list = []
    errors = {}

    for member in members:
        member_name = member if isinstance(member, str) else member.get("character_name")
        if not member_name:
            logger.warning(f"잘못된 길드원 데이터 발견: {member}")
            continue

        try:
            ocid = character_api.get_character_ocid(member_name)
        except Exception as e:
            errors[member_name] = f"OCID 조회 실패 - {e}"
            logger.error(f"OCID 조회 실패: {member_name} - {e}")
            continue  # OCID 조회 실패 시 해당 캐릭터는 조회하지 않음

        try:
            char_info = character_api.get_character_basic(ocid, previous_date)
            min_stat_attack = character_api.get_character_stat(ocid, previous_date) or 0.0  # None이면 0.0으로 설정
            union_level = character_api.get_union_info(ocid, previous_date) or 0  # None이면 0으로 설정

            char_info.update({"min_stat_attack": min_stat_attack, "union_level": union_level})

            logger.info(f"캐릭터 조회 성공: {member_name} (OCID: {ocid})")
        except Exception as e:
            errors[member_name] = f"캐릭터 정보 조회 실패 - {e}"
            logger.error(f"캐릭터 정보 조회 실패: {member_name} - {e}")
            char_info = {"character_name": member_name, "error": str(e)}

        character_info_list.append(char_info)

    # 3. 통계 집계
    stats = aggregate_guild_stats(character_info_list)
    logger.info(f"길드원 데이터 집계 완료: {guild_name}")

    # 4. 결과 반환
    result = {"guild_info": guild_info, "aggregated_stats": stats, "errors": errors}
    logger.info(f"길드 대시보드 응답 완료: {guild_name}")

    return JSONResponse(content=result)

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger

from src.api import character as character_api
from src.api import guild as guild_api
from src.stats.aggregator import aggregate_guild_stats
from src.utils import get_previous_date


# 로깅 설정 (파일 저장 및 콘솔 출력)
logger.add("guild_dashboard.log", rotation="10 MB", level="INFO")

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
    guild_name: str = Query(..., description="길드 이름"),
    world_name: str = Query(..., description="월드 이름"),
    previous_date: str = Depends(get_previous_date),
):
    """
    1. 어제 날짜를 기준으로 길드 ID와 기본 정보를 조회
    2. 길드원 각각의 개인 식별자(ocid) 및 기본 정보를 조회
    3. 조회된 길드원 정보를 집계하여 통계(평균 레벨, 클래스 분포, 성별 분포 등)를 계산
    4. 길드 기본 정보, 집계 결과, 에러 정보를 JSON 형태로 반환
    """
    logger.info(f"길드 조회 요청: {guild_name} ({world_name}), 기준 날짜: {previous_date}")

    try:
        # 1. 길드 ID 및 기본 정보 조회
        oguild_id = guild_api.get_guild_id(guild_name, world_name)
        guild_info = guild_api.get_guild_basic(oguild_id, previous_date)
        logger.info(f"길드 정보 조회 성공: {guild_name} (ID: {oguild_id})")
    except Exception as e:
        logger.error(f"길드 정보 조회 실패: {e}")
        raise HTTPException(status_code=400, detail=f"길드 정보 조회 실패: {e}")

    # 2. 각 길드원 개별 정보 조회
    members = guild_info.get("guild_member", [])
    character_info_list = []
    errors = {}

    for member_name in members:
        try:
            ocid = character_api.get_character_ocid(member_name)
            char_info = character_api.get_character_basic(ocid, previous_date)
            logger.info(f"캐릭터 조회 성공: {member_name} (OCID: {ocid})")
        except Exception as e:
            errors[member_name] = str(e)
            logger.error(f"캐릭터 조회 실패: {member_name} - {e}")
            char_info = {"character_name": member_name, "error": str(e)}

        character_info_list.append(char_info)

    # 3. 통계 집계 (예: 평균 레벨, 클래스 분포, 성별 분포 등)
    stats = aggregate_guild_stats(character_info_list)
    logger.info(f"길드원 데이터 집계 완료: {guild_name}")

    # 4. 결과 반환
    result = {"guild_info": guild_info, "aggregated_stats": stats, "errors": errors}
    logger.info(f"길드 대시보드 응답 완료: {guild_name}")

    return JSONResponse(content=result)

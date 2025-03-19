import os

from dotenv import load_dotenv


# .env 파일 로드
load_dotenv()


def get_env_variable(var_name):
    """환경 변수를 가져오고, 없을 경우 에러 발생"""
    value = os.getenv(var_name)
    if value is None:
        raise EnvironmentError(f"환경 변수 {var_name}가 설정되지 않았습니다.")
    return value


# 필수 환경 변수 불러오기 (없으면 예외 발생)
API_KEY = get_env_variable("API_KEY")
BASE_URL = get_env_variable("BASE_URL")

# 선택적 환경 변수 불러오기 (기본값 설정 가능)
GUILD_ID_URL = f"{BASE_URL}{get_env_variable('GUILD_ID_ENDPOINT')}"
GUILD_BASIC_URL = f"{BASE_URL}{get_env_variable('GUILD_BASIC_ENDPOINT')}"
CHARACTER_ID_URL = f"{BASE_URL}{get_env_variable('CHARACTER_ID_ENDPOINT')}"
CHARACTER_BASIC_URL = f"{BASE_URL}{get_env_variable('CHARACTER_BASIC_ENDPOINT')}"
CHARACTER_FINAL_STAT_URL = f"{BASE_URL}{get_env_variable('CHARACTER_FIANL_STAT')}"
CHARACTER_UNION_INFO_URL = f"{BASE_URL}{get_env_variable('CHARACTER_UNION_INFO')}"

# API 요청 제한 설정 (기본값 제공)
REQUEST_LIMIT = int(os.getenv("REQUEST_LIMIT", 4))  # 기본값 4
DAILY_LIMIT = int(os.getenv("DAILY_LIMIT", 1000))  # 기본값 1000

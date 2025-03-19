import os

from dotenv import load_dotenv


# .env 파일 로드
load_dotenv()

# 환경 변수 불러오기
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

# 길드 관련 API 엔드포인트
GUILD_ID_URL = f"{BASE_URL}{os.getenv('GUILD_ID_ENDPOINT')}"
GUILD_BASIC_URL = f"{BASE_URL}{os.getenv('GUILD_BASIC_ENDPOINT')}"

# 캐릭터 관련 API 엔드포인트
CHARACTER_ID_URL = f"{BASE_URL}{os.getenv('CHARACTER_ID_ENDPOINT')}"
CHARACTER_BASIC_URL = f"{BASE_URL}{os.getenv('CHARACTER_BASIC_ENDPOINT')}"

# API 요청 제한 설정
REQUEST_LIMIT = int(os.getenv("REQUEST_LIMIT", 4))  # 기본값 4
DAILY_LIMIT = int(os.getenv("DAILY_LIMIT", 1000))  # 기본값 1000

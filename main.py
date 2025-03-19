# main.py

from src.api import character as character_api
from src.api import guild as guild_api
from src.dashboard.dashboard import display_dashboard
from src.stats.aggregator import aggregate_guild_stats
from src.utils import get_previous_date


def main():
    # 사용자로부터 길드명과 월드 입력 받기
    guild_name = input("길드 이름을 입력하세요: ")
    world_name = input("월드를 입력하세요: ")

    # 어제 날짜 사용
    previous_date = get_previous_date()

    # 1. 길드 ID 조회
    print("길드 ID 조회 중...")
    oguild_id = guild_api.get_guild_id(guild_name, world_name)
    print(f"조회된 길드 ID: {oguild_id}")

    # 2. 길드 기본 정보 조회
    print("길드 기본 정보 조회 중...")
    guild_info = guild_api.get_guild_basic(oguild_id, previous_date)
    print(f"길드 정보 조회 완료: {guild_info.get('guild_name')}")

    # 3. 각 길드원 개별 정보 조회
    members = guild_info.get("guild_member", [])
    character_info_list = []
    print("길드원 개별 정보 조회 중...")
    for member_name in members:
        try:
            ocid = character_api.get_character_ocid(member_name)
            char_info = character_api.get_character_basic(ocid, previous_date)
            character_info_list.append(char_info)
            print(f"조회 완료: {member_name}")
        except Exception as e:
            print(f"에러 발생 ({member_name}): {e}")

    # 4. 통계(aggregated features) 계산
    stats = aggregate_guild_stats(character_info_list)

    # 5. 대시보드 출력
    display_dashboard(guild_info, stats)


if __name__ == "__main__":
    main()

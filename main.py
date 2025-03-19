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
    try:
        oguild_id = guild_api.get_guild_id(guild_name, world_name)
        print(f"조회된 길드 ID: {oguild_id}")
    except Exception as e:
        # 에러 메시지를 UTF-8로 강제 변환하여 출력
        error_message = str(e).encode("utf-8", errors="replace").decode("utf-8")
        print(f"길드 ID 조회 실패: {error_message}")
        return

    # 2. 길드 기본 정보 조회
    print("길드 기본 정보 조회 중...")
    try:
        guild_info = guild_api.get_guild_basic(oguild_id, previous_date)
        print(f"길드 정보 조회 완료: {guild_info.get('guild_name', 'Unknown')}")
    except Exception as e:
        error_message = str(e).encode("utf-8", errors="replace").decode("utf-8")
        print(f"길드 기본 정보 조회 실패: {error_message}")
        return

    # 3. 각 길드원 개별 정보 조회
    members = guild_info.get("guild_member", [])
    character_info_list = []
    print("길드원 개별 정보 조회 중...")
    for member_name in members:
        try:
            ocid = character_api.get_character_ocid(member_name)

            # 기본 캐릭터 정보 조회
            char_info = character_api.get_character_basic(ocid, previous_date)

            # 최소 스탯 공격력 조회
            try:
                min_stat_attack = character_api.get_character_stat(ocid, previous_date)
                char_info["min_stat_attack"] = min_stat_attack
            except Exception as e:
                print(f"스탯 정보 조회 실패 ({member_name}): {str(e)}")
                char_info["min_stat_attack"] = None

            # 유니온 레벨 조회
            try:
                union_level = character_api.get_union_info(ocid, previous_date)
                char_info["union_level"] = union_level
            except Exception as e:
                print(f"유니온 정보 조회 실패 ({member_name}): {str(e)}")
                char_info["union_level"] = None

            character_info_list.append(char_info)
            print(f"조회 완료: {member_name}")
        except Exception as e:
            error_message = str(e).encode("utf-8", errors="replace").decode("utf-8")
            print(f"기본 정보 조회 실패 ({member_name}): {error_message}")

    # 4. 통계(aggregated features) 계산
    print("통계 계산 중...")
    stats = aggregate_guild_stats(character_info_list)
    print("통계 계산 완료!")

    # 간단한 통계 요약 출력
    print("\n===== 길드 통계 요약 =====")
    print(f"총 길드원 수: {stats['total_members']}명")
    print(f"평균 레벨: {stats['average_level']:.2f}")
    print(f"평균 최소 스탯 공격력: {stats['average_min_stat_attack']:.2f}")
    print(f"평균 유니온 레벨: {stats['average_union_level']:.2f}")
    print(f"평균 캐릭터 생성일(일 수): {stats['average_character_age_days']:.2f}일")

    # 5. 대시보드 출력
    display_dashboard(guild_info, stats)


if __name__ == "__main__":
    main()

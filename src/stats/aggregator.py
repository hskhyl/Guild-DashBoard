from datetime import datetime

from dateutil import parser


def aggregate_guild_stats(character_info_list):
    """
    캐릭터 정보 리스트를 받아 길드 통계를 계산하는 함수.
    - 평균 레벨
    - 평균 경험치
    - 평균 최소 스탯 공격력
    - 평균 유니온 레벨
    - 클래스 분포
    - 성별 분포
    - 평균 캐릭터 생성일 (현재일 - 생성일)
    """
    if not character_info_list:
        return {}

    total_level = total_exp = total_min_stat_attack = total_union_level = 0
    total_days_since_creation = 0
    valid_stat_count = valid_union_count = valid_creation_count = 0
    class_distribution = {}
    gender_distribution = {}
    today = datetime.now()
    count = len(character_info_list)

    for char in character_info_list:
        # 기본 정보 집계
        total_level += char.get("character_level", 0)
        total_exp += char.get("character_exp", 0)

        # 최소 스탯 공격력 평균 계산
        min_stat_attack = char.get("min_stat_attack")
        if min_stat_attack is not None and isinstance(min_stat_attack, (int, float)) and min_stat_attack > 0:
            total_min_stat_attack += min_stat_attack
            valid_stat_count += 1

        # 유니온 레벨 평균 계산
        union_level = char.get("union_level")
        if union_level is not None and isinstance(union_level, int) and union_level > 0:
            total_union_level += union_level
            valid_union_count += 1

        # 클래스 및 성별 분포 집계
        class_name = char.get("character_class", "Unknown")
        class_distribution[class_name] = class_distribution.get(class_name, 0) + 1

        gender = char.get("character_gender", "Unknown")
        gender_distribution[gender] = gender_distribution.get(gender, 0) + 1

        # 캐릭터 생성일 계산
        char_create_date = char.get("character_date_create")
        if char_create_date:
            try:
                created_date = parser.parse(char_create_date)
                # 타임존 정보 제거하여 naive datetime으로 만들기
                if created_date.tzinfo is not None:
                    created_date = created_date.replace(tzinfo=None)

                days_since = (today - created_date).days
                if days_since >= 0:  # 음수 값은 제외
                    total_days_since_creation += days_since
                    print("디버그:", total_days_since_creation)
                    valid_creation_count += 1
            except Exception as e:
                print(f"날짜 변환 오류: {e}")
                pass

    # 최종 통계 계산
    return {
        "total_members": count,
        "average_level": total_level / count if count else 0,
        "average_experience": total_exp / count if count else 0,
        "average_min_stat_attack": total_min_stat_attack / valid_stat_count if valid_stat_count else 0,
        "average_union_level": total_union_level / valid_union_count if valid_union_count else 0,
        "average_character_age_days": total_days_since_creation / valid_creation_count if valid_creation_count else 0,
        "class_distribution": class_distribution,
        "gender_distribution": gender_distribution,
    }

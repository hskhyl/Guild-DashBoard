# src/stats/aggregator.py


def aggregate_guild_stats(character_info_list):
    """
    캐릭터 정보 리스트를 받아 길드 통계 계산
    - 평균 레벨
    - 평균 경험치
    - 클래스 분포
    - 성별 분포
    """
    if not character_info_list:
        return {}

    total_level = 0
    total_exp = 0
    class_distribution = {}
    gender_distribution = {}
    count = len(character_info_list)

    for char in character_info_list:
        level = char.get("character_level", 0)
        total_level += level

        exp = char.get("character_exp", 0)
        total_exp += exp

        # 클래스 분포 집계
        char_class = char.get("character_class", "Unknown")
        class_distribution[char_class] = class_distribution.get(char_class, 0) + 1

        # 성별 분포 집계
        gender = char.get("character_gender", "Unknown")
        gender_distribution[gender] = gender_distribution.get(gender, 0) + 1

    average_level = total_level / count
    average_exp = total_exp / count

    stats = {
        "total_members": count,
        "average_level": average_level,
        "average_experience": average_exp,
        "class_distribution": class_distribution,
        "gender_distribution": gender_distribution,
    }
    return stats

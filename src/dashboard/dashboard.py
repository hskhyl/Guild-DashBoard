def display_dashboard(guild_info, stats):
    """길드 대시보드 출력"""
    print("=== Guild Information ===")
    print(f"Guild Name: {guild_info.get('guild_name', 'Unknown')}")
    print(f"World: {guild_info.get('world_name', 'Unknown')}")
    print(f"Guild Level: {guild_info.get('guild_level', 0)}")
    print(f"Guild Fame: {guild_info.get('guild_fame', 0)}")
    print(f"Guild Point: {guild_info.get('guild_point', 0)}")
    print(f"Guild Master: {guild_info.get('guild_master_name', 'Unknown')}")
    print(f"Guild Member Count (API): {guild_info.get('guild_member_count', 0)}\n")

    print("=== Aggregated Member Stats ===")
    print(f"Total Members Retrieved: {stats.get('total_members', 0)}")
    print(f"Average Level: {stats.get('average_level', 0.0):.2f}")
    print(f"Average Experience: {stats.get('average_experience', 0.0):.2f}")
    print(f"Average Union Level: {stats.get('average_union_level', 0.0):.2f}")  # ✅ 유니온 레벨 추가
    print(f"Average Min Stat Attack: {stats.get('average_min_stat_attack', 0.0):.2f}")  # ✅ 스탯 공격력 추가
    print(f"Average Character Age (Days): {stats.get('average_character_age_days', 0.0):.2f}")  # ✅ 생성일 평균 추가

    # 직업 분포 출력
    print("\n=== Class Distribution ===")
    class_distribution = stats.get("class_distribution", {})
    if class_distribution:
        for cls, cnt in class_distribution.items():
            print(f" - {cls}: {cnt}")
    else:
        print(" - No data available")

    # 성별 분포 출력
    print("\n=== Gender Distribution ===")
    gender_distribution = stats.get("gender_distribution", {})
    if gender_distribution:
        for gender, cnt in gender_distribution.items():
            print(f" - {gender}: {cnt}")
    else:
        print(" - No data available")

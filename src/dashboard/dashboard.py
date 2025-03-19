# src/dashboard/dashboard.py


def display_dashboard(guild_info, stats):
    print("=== Guild Dashboard ===")
    print(f"Guild Name: {guild_info.get('guild_name')}")
    print(f"World: {guild_info.get('world_name')}")
    print(f"Guild Level: {guild_info.get('guild_level')}")
    print(f"Guild Fame: {guild_info.get('guild_fame')}")
    print(f"Guild Point: {guild_info.get('guild_point')}")
    print(f"Guild Master: {guild_info.get('guild_master_name')}")
    print(f"Guild Member Count (API): {guild_info.get('guild_member_count')}\n")

    print("=== Aggregated Member Stats ===")
    print(f"Total Members Retrieved: {stats.get('total_members')}")
    print(f"Average Level: {stats.get('average_level'):.2f}")
    print(f"Average Experience: {stats.get('average_experience'):.2f}")
    print("\nClass Distribution:")
    for cls, cnt in stats.get("class_distribution", {}).items():
        print(f" - {cls}: {cnt}")

    print("\nGender Distribution:")
    for gender, cnt in stats.get("gender_distribution", {}).items():
        print(f" - {gender}: {cnt}")

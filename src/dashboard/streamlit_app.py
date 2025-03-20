from datetime import datetime

import pandas as pd
import plotly.express as px
import requests
import streamlit as st


# 페이지 기본 설정
st.set_page_config(page_title="메이플스토리 길드 대시보드", layout="wide", initial_sidebar_state="expanded")

st.title("🏰 메이플스토리 길드 분석 대시보드")

# 🌟 사이드바: 길드 정보 입력
with st.sidebar:
    st.header("🎯 길드 정보 입력")
    world_name = st.selectbox(
        "🌍 월드 선택",
        [
            "스카니아",
            "베라",
            "루나",
            "제니스",
            "크로아",
            "유니온",
            "엘리시움",
            "이노시스",
            "레드",
            "오로라",
            "아케인",
            "노바",
        ],
    )
    guild_name = st.text_input("🏹 길드 이름", placeholder="길드 이름을 입력하세요")

    with st.form(key="guild_form"):
        submit_button = st.form_submit_button("🚀 길드 정보 조회")

    if submit_button:
        if guild_name:
            api_url = "http://localhost:8000/guild"
            with st.spinner("🔄 길드 정보를 불러오는 중..."):
                try:
                    response = requests.get(api_url, params={"world_name": world_name, "guild_name": guild_name})
                    if response.status_code == 200:
                        st.session_state.guild_data = response.json()
                        st.success("✅ 길드 정보를 성공적으로 불러왔습니다!")
                    else:
                        st.error(f"⚠ 오류 발생: {response.status_code}")
                except requests.RequestException as e:
                    st.error(f"🔌 서버 연결 오류: {e}")
        else:
            st.warning("⚠ 길드 이름을 입력해주세요.")

# 📊 메인 페이지
if "guild_data" in st.session_state:
    data = st.session_state.guild_data
    guild_info = data["guild_info"]
    stats = data["aggregated_stats"]

    # 🔹 길드 기본 정보
    st.markdown("### 🏰 길드 기본 정보")
    col1, col2, col3 = st.columns(3)
    col1.metric("🏆 길드 레벨", guild_info["guild_level"])
    col2.metric("🔥 길드 명성도", f"{guild_info['guild_fame']:,}")
    col3.metric("💎 길드 포인트", f"{guild_info['guild_point']:,}")

    st.markdown(f"#### 👑 길드마스터: `{guild_info['guild_master_name']}`")
    st.caption(f"📅 정보 갱신: {datetime.fromisoformat(guild_info['date']).strftime('%Y-%m-%d')}")

    # 🔹 길드원 통계
    st.markdown("---")
    st.markdown("### 📈 길드원 통계")
    col1, col2, col3 = st.columns(3)
    col1.metric("🎯 평균 레벨", f"{stats['average_level']:.2f}")
    col2.metric("🌟 평균 유니온 레벨", f"{stats['average_union_level']:.2f}")
    col3.metric("⏳ 평균 캐릭터 나이(일)", f"{stats['average_character_age_days']:.2f}")

    # 🔹 직업 분포 차트
    st.markdown("### 🎭 직업 분포")
    class_data = pd.DataFrame(
        {"직업": list(stats["class_distribution"].keys()), "인원 수": list(stats["class_distribution"].values())}
    ).sort_values(by="인원 수", ascending=False)

    fig = px.bar(
        class_data, x="직업", y="인원 수", color="인원 수", color_continuous_scale=px.colors.sequential.Plasma
    )
    fig.update_layout(height=400, margin={"l": 10, "r": 10, "t": 30, "b": 10})
    st.plotly_chart(fig, use_container_width=True)

    # 🔹 성별 분포 파이 차트
    st.markdown("### 👫 성별 분포")
    gender_data = pd.DataFrame(
        {"성별": list(stats["gender_distribution"].keys()), "인원 수": list(stats["gender_distribution"].values())}
    )

    fig = px.pie(
        gender_data, values="인원 수", names="성별", hole=0.3, color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(fig, use_container_width=True)

    # 📜 길드원 목록 (필요할 때만 펼쳐서 보기)
    with st.expander("📜 전체 길드원 목록 보기"):
        if "guild_member" in guild_info and len(guild_info["guild_member"]) > 0:
            st.dataframe(guild_info["guild_member"])
        else:
            st.info("길드원 상세 정보가 없습니다.")

else:
    st.info("👈 좌측에서 월드와 길드 이름을 입력하고 '길드 정보 조회'를 눌러주세요.")

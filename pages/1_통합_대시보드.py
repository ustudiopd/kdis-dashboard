"""
통합 대시보드 페이지
재학생 현황 및 MOU 현황 시각화
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from utils.github_handler import load_data

st.set_page_config(
    page_title="통합 대시보드",
    page_icon="📊",
    layout="wide"
)

st.title("📊 통합 대시보드")

# 데이터 로드
data = load_data("dashboard_data.json")

if not data:
    st.error("❌ 데이터를 불러올 수 없습니다.")
    st.stop()

# KPI 표시
st.header("📈 주요 지표 (KPI)")

kpi = data.get("kpi", {})
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="재학생 수",
        value=f"{kpi.get('total_students', 0):,}명"
    )

with col2:
    st.metric(
        label="파트너 기관 수",
        value=f"{kpi.get('partners', 0):,}개"
    )

with col3:
    st.metric(
        label="취업률",
        value=f"{kpi.get('employment_rate', 0):.1f}%"
    )

# 재학생 현황 (Pie Chart)
st.markdown("---")
st.header("🌍 지역별 재학생 현황")

students_by_region = data.get("students_by_region", [])
if students_by_region:
    df_region = pd.DataFrame(students_by_region)
    
    fig_pie = px.pie(
        df_region,
        values='count',
        names='region',
        title='지역별 재학생 분포',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # 데이터 테이블
    with st.expander("📋 상세 데이터"):
        st.dataframe(df_region, use_container_width=True)
else:
    st.info("데이터가 없습니다.")

# MOU 현황 (Bar Chart)
st.markdown("---")
st.header("🤝 MOU 파트너 현황")

mou_partners = data.get("mou_partners", [])
if mou_partners:
    df_mou = pd.DataFrame(mou_partners)
    
    fig_bar = px.bar(
        df_mou,
        x='name',
        y='year',
        color='country',
        title='MOU 파트너 기관 (체결 연도)',
        labels={'name': '기관명', 'year': '체결 연도', 'country': '국가'},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_bar.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # 데이터 테이블
    with st.expander("📋 상세 데이터"):
        st.dataframe(df_mou, use_container_width=True)
else:
    st.info("데이터가 없습니다.")


"""
KDI 스마트 행정 플랫폼 - 메인 앱
Streamlit Multi-page Application
"""

import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="KDI 스마트 행정 플랫폼",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 사이드바
with st.sidebar:
    st.title("🏛️ KDI 스마트 행정 플랫폼")
    st.markdown("---")
    
    st.markdown("### 📋 메뉴")
    
    # Streamlit 페이지는 자동으로 사이드바에 표시되므로
    # 여기서는 간단한 안내만 제공
    st.info("""
    사이드바 하단의 페이지 메뉴를 통해
    각 기능에 접근할 수 있습니다.
    """)
    
    st.markdown("**주요 기능:**")
    st.markdown("""
    - 📊 통합 대시보드
    - 🤖 주간보고 AI 챗봇
    - 📅 스마트 일정 관리
    - 👥 직원 추천 시스템
    - 📋 기관평가 코칭
    - 💼 명함 공유 허브
    - 🔧 데이터 관리 (Admin)
    """)
    
    st.markdown("---")
    st.markdown("### ℹ️ 정보")
    st.caption("GitHub를 DB처럼 활용하는 스마트 행정 플랫폼")

# 메인 페이지
st.title("🏛️ KDI 스마트 행정 플랫폼")
st.markdown("### 환영합니다!")

st.info("""
이 플랫폼은 GitHub Repository를 데이터베이스처럼 활용하여 
서버 비용 없이 데이터를 관리하고 팀원들과 공유할 수 있는 시스템입니다.

**주요 기능:**
- 📊 통합 대시보드: 재학생 현황, MOU 현황 시각화
- 🤖 주간보고 AI 챗봇: 키워드 기반 보고서 검색
- 📅 스마트 일정 관리: 직원별 일정 및 공통 빈 시간 찾기
- 👥 직원 추천 시스템: 전문성 기반 직원 검색
- 📋 기관평가 코칭: 평가 항목별 가이드라인 제공
- 💼 명함 공유 허브: 외부 기관 담당자 정보 관리
- 🔧 데이터 관리: JSON 파일 업로드 및 GitHub 저장

사이드바 메뉴를 통해 각 기능에 접근할 수 있습니다.
""")

st.markdown("---")
st.caption("© 2024 KDI School. All rights reserved.")


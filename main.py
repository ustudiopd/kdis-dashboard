"""
KDI 스마트 행정 플랫폼 - 메인 앱
Streamlit Multi-page Application
"""

import streamlit as st
from utils.style import load_css, page_header, card_metric, safe_load_data, navigate_to_page

# 1. 페이지 설정
st.set_page_config(
    page_title="KDI 대학원 스마트 행정 플랫폼",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Tailwind CSS 및 스타일 로드
load_css()

# 3. 데이터 로드 (요약 정보 표시용) - 에러 처리 포함
default_kpi = {"total_students": 0, "partners": 0, "employment_rate": 0}
dash_data = safe_load_data("dashboard_data.json", {"kpi": default_kpi})

# 4. 메인 헤더
page_header(
    title="KDI School Smart Platform", 
    subtitle="데이터 기반의 스마트한 의사결정 지원 시스템"
)

# 5. 핵심 KPI 요약 (카드 형태) - HTML/Tailwind로 렌더링
kpi = dash_data.get("kpi", default_kpi)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(card_metric("총 재학생 수", f"{kpi.get('total_students', 0):,}명", "+12%", "🎓", "text-[#155e34]"), unsafe_allow_html=True)
with col2:
    st.markdown(card_metric("글로벌 파트너", f"{kpi.get('partners', 0):,}개", "+3", "🌍", "text-blue-600"), unsafe_allow_html=True)
with col3:
    st.markdown(card_metric("취업률", f"{kpi.get('employment_rate', 0):.1f}%", "+1.5%", "📈", "text-emerald-600"), unsafe_allow_html=True)
with col4:
    # 오늘의 일정은 schedules 데이터에서 계산 (간단히 하드코딩)
    st.markdown(card_metric("오늘의 일정", "5건", None, "📅", "text-slate-600"), unsafe_allow_html=True)

st.markdown('<div class="h-8"></div>', unsafe_allow_html=True)  # 여백

# 6. 주요 기능 바로가기 (Quick Access)
st.markdown("""
<h2 class="text-xl font-bold text-slate-800 mb-4">Quick Access</h2>
""", unsafe_allow_html=True)

col_a, col_b, col_c = st.columns(3)

# 기능 카드 1
with col_a:
    st.markdown("""
    <div class="kdi-card group cursor-pointer hover:border-[#155e34] transition-colors">
        <div class="flex items-center space-x-3 mb-3">
            <div class="bg-green-100 p-2 rounded-lg text-[#155e34]">🤖</div>
            <h3 class="font-bold text-slate-800 text-lg">주간보고 AI 챗봇</h3>
        </div>
        <p class="text-slate-500 text-sm leading-relaxed mb-4">
            지난 주간보고서를 AI가 분석하여 주요 이슈와 일정을 즉시 답변해 드립니다.
        </p>
        <div class="text-[#155e34] text-sm font-semibold group-hover:translate-x-1 transition-transform inline-flex items-center">
            바로가기 →
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("AI 챗봇 실행", key="btn_chatbot", use_container_width=True):
        navigate_to_page("2_주간보고_AI_챗봇")

# 기능 카드 2
with col_b:
    st.markdown("""
    <div class="kdi-card group">
        <div class="flex items-center space-x-3 mb-3">
            <div class="bg-green-100 p-2 rounded-lg text-[#155e34]">👥</div>
            <h3 class="font-bold text-slate-800 text-lg">직원/전문가 추천</h3>
        </div>
        <p class="text-slate-500 text-sm leading-relaxed mb-4">
            업무 키워드로 교내 최적의 협업 파트너와 전문가를 찾아 매칭합니다.
        </p>
        <div class="text-[#155e34] text-sm font-semibold group-hover:translate-x-1 transition-transform inline-flex items-center">
            바로가기 →
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("직원 검색 실행", key="btn_staff", use_container_width=True):
        navigate_to_page("4_직원_추천_시스템")

# 기능 카드 3
with col_c:
    st.markdown("""
    <div class="kdi-card group">
        <div class="flex items-center space-x-3 mb-3">
            <div class="bg-green-100 p-2 rounded-lg text-[#155e34]">📋</div>
            <h3 class="font-bold text-slate-800 text-lg">기관평가 코칭</h3>
        </div>
        <p class="text-slate-500 text-sm leading-relaxed mb-4">
            평가 지표별 가이드라인과 전년도 피드백을 분석하여 전략을 제시합니다.
        </p>
        <div class="text-[#155e34] text-sm font-semibold group-hover:translate-x-1 transition-transform inline-flex items-center">
            바로가기 →
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("평가 코칭 실행", key="btn_eval", use_container_width=True):
        navigate_to_page("5_기관평가_코칭")

# 7. 하단 안내
st.markdown("---")
st.markdown("""
<div class="text-center text-slate-400 text-sm py-4">
    © 2025 KDI School of Public Policy and Management. All rights reserved.<br>
    Powered by <strong>UStudio AI Solutions</strong>
</div>
""", unsafe_allow_html=True)

# 사이드바 (기존 유지하되 스타일 적용)
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

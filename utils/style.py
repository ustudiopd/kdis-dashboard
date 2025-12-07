"""
KDI 스마트 행정 플랫폼 - 스타일 모듈
KDI 대학원 브랜드 컬러(Green & Charcoal) 적용
"""

import streamlit as st
from utils.github_handler import load_data
from typing import Dict, Any, Optional


def load_css():
    """
    KDI 대학원 브랜드 컬러(Green & Charcoal)가 적용된 Tailwind CSS 스타일을 주입합니다.
    """
    # KDI 브랜드 컬러 정의
    KDI_GREEN = "#155e34"       # 메인 짙은 녹색
    KDI_ACCENT = "#2ecc71"      # 포인트 밝은 녹색
    KDI_DARK = "#1f2937"        # 본문/제목 다크 그레이
    BG_COLOR = "#f8fafc"        # 배경색

    st.markdown(f"""
        <script src="https://cdn.tailwindcss.com"></script>
        
        <style>
            /* 1. 폰트 및 기본 배경 설정 */
            @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
            
            html, body, [class*="css"] {{
                font-family: 'Pretendard', -apple-system, system-ui, sans-serif !important;
            }}
            
            .stApp {{
                background-color: {BG_COLOR}; 
            }}

            /* 2. Streamlit 기본 요소 오버라이딩 */
            /* 상단 헤더 숨김 */
            header[data-testid="stHeader"] {{
                visibility: hidden;
            }}
            
            /* 메인 컨테이너 패딩 조절 */
            .main .block-container {{
                padding-top: 2rem;
                padding-bottom: 5rem;
                max-width: 1200px;
            }}
            
            /* 사이드바 스타일 */
            section[data-testid="stSidebar"] {{
                background-color: #ffffff;
                border-right: 1px solid #e5e7eb;
            }}
            
            /* 버튼 스타일 (KDI Green 적용) */
            div.stButton > button {{
                background-color: {KDI_GREEN} !important;
                color: white !important;
                border: none !important;
                border-radius: 6px !important;
                padding: 0.5rem 1rem !important;
                transition: all 0.2s !important;
            }}
            div.stButton > button:hover {{
                background-color: #14532d !important; /* 더 짙은 녹색 */
                transform: translateY(-1px);
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }}

            /* 3. 커스텀 컴포넌트 스타일 */
            
            /* KDI 카드: 상단에 녹색 포인트 라인 추가 */
            .kdi-card {{
                background-color: white;
                border-radius: 0.5rem;
                padding: 1.5rem;
                box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
                border: 1px solid #f1f5f9;
                border-top: 4px solid {KDI_GREEN}; /* 핵심 포인트 */
                height: 100%;
                transition: all 0.2s ease-in-out;
            }}
            .kdi-card:hover {{
                transform: translateY(-2px);
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            }}
            
            .kdi-header {{
                color: {KDI_GREEN};
                font-weight: 800;
                letter-spacing: -0.025em;
            }}
            
            .kdi-subtext {{
                color: #64748b;
            }}

            /* 메트릭 숫자 강조 */
            .metric-value {{
                color: {KDI_DARK};
                font-feature-settings: "tnum";
            }}
        </style>
    """, unsafe_allow_html=True)


def card_metric(label: str, value: str, diff: Optional[str] = None, icon: str = "📊", color: str = "text-[#155e34]") -> str:
    """
    KDI 테마가 적용된 메트릭 카드
    
    Args:
        label: 메트릭 라벨
        value: 메트릭 값
        diff: 변화량 (선택적, 예: "+12%")
        icon: 아이콘 이모지
        color: 아이콘 색상 클래스 (기본값: KDI Green)
    
    Returns:
        HTML 문자열
    """
    diff_html = ""
    if diff:
        # 상승/하락에 따른 색상
        is_pos = "+" in str(diff)
        diff_color = "text-emerald-600 bg-emerald-50" if is_pos else "text-rose-600 bg-rose-50"
        diff_icon = "▲" if is_pos else "▼"
        diff_html = f'<span class="text-xs font-bold {diff_color} px-2 py-1 rounded-full ml-2 flex items-center gap-1">{diff_icon} {diff}</span>'
        
    return f'<div class="kdi-card flex flex-col justify-between"><div><div class="flex items-center justify-between mb-3"><span class="text-sm font-semibold text-slate-500 uppercase tracking-wider">{label}</span><span class="text-xl p-2 bg-slate-100 rounded-lg {color}">{icon}</span></div><div class="flex items-baseline mt-1"><span class="text-3xl font-bold text-slate-900 tracking-tight metric-value">{value}</span>{diff_html}</div></div></div>'


def page_header(title: str, subtitle: str) -> None:
    """
    KDI 홈페이지 헤더 스타일을 차용한 페이지 타이틀
    
    Args:
        title: 페이지 제목
        subtitle: 페이지 부제목
    """
    st.markdown(f"""
    <div class="mb-8 bg-white p-6 rounded-lg border-l-4 border-[#155e34] shadow-sm">
        <h1 class="text-3xl font-extrabold text-[#1f2937] tracking-tight">{title}</h1>
        <p class="text-slate-500 mt-2 text-lg font-medium">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def badge(text: str, color: str = "bg-green-100 text-green-800") -> str:
    """
    배지 컴포넌트
    
    Args:
        text: 배지 텍스트
        color: 색상 클래스
    
    Returns:
        HTML 문자열
    """
    return f'<span class="px-2.5 py-0.5 rounded-full text-xs font-medium {color}">{text}</span>'


def safe_load_data(filename: str, default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    안전한 데이터 로드 함수 (에러 처리 포함)
    
    Args:
        filename: 로드할 파일명
        default: 기본값 (데이터 로드 실패 시)
    
    Returns:
        로드된 데이터 또는 기본값
    """
    try:
        data = load_data(filename)
        if not data:
            if default is not None:
                return default
            return {}
        return data
    except Exception as e:
        st.warning(f"⚠️ 데이터 로드 중 오류 발생: {e}. 기본값을 사용합니다.")
        if default is not None:
            return default
        return {}


def navigate_to_page(page_name: str) -> None:
    """
    페이지 전환 헬퍼 함수 (에러 처리 포함)
    
    Args:
        page_name: 페이지 이름 (예: "2_주간보고_AI_챗봇")
    """
    try:
        # Streamlit 페이지 전환은 pages/ 경로 사용
        page_path = f"pages/{page_name}"
        st.switch_page(page_path)
    except Exception as e:
        st.error(f"❌ 페이지 전환 실패: {e}")
        st.info("사이드바 메뉴를 통해 페이지로 이동해주세요.")

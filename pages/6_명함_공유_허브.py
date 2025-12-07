"""
명함 공유 허브 페이지
외부 기관 담당자 정보 검색 및 관리
"""

import streamlit as st
import pandas as pd
from utils.github_handler import load_data

st.set_page_config(
    page_title="명함 공유 허브",
    page_icon="💼",
    layout="wide"
)

st.title("💼 명함 공유 허브")

# 데이터 로드
business_cards = load_data("business_cards.json")

if not business_cards:
    st.error("❌ 데이터를 불러올 수 없습니다.")
    st.stop()

st.info("""
외부 기관 담당자 정보를 검색하고 관리할 수 있습니다.
기관명, 담당자명, 또는 이력으로 검색하세요.
""")

# 검색 기능
st.markdown("---")
st.header("🔍 담당자 검색")

search_keyword = st.text_input(
    "검색어를 입력하세요 (기관명, 담당자명, 이력 등)",
    placeholder="예: World Bank, UNESCO, 입학설명회"
)

# 검색 함수
def search_cards(keyword: str, cards: list) -> list:
    """키워드 기반 명함 검색"""
    if not keyword:
        return cards
    
    keyword_lower = keyword.lower()
    results = []
    
    for card in cards:
        score = 0
        # 기관명 매칭
        if keyword_lower in card.get("org", "").lower():
            score += 10
        # 담당자명 매칭
        if keyword_lower in card.get("name", "").lower():
            score += 8
        # 직책 매칭
        if keyword_lower in card.get("position", "").lower():
            score += 5
        # 이력 매칭
        if keyword_lower in card.get("history", "").lower():
            score += 6
        
        if score > 0:
            results.append((card, score))
    
    # 점수순 정렬
    results.sort(key=lambda x: x[1], reverse=True)
    return [r[0] for r in results]

# 검색 결과
if search_keyword:
    results = search_cards(search_keyword, business_cards)
    st.info(f"'{search_keyword}' 검색 결과: {len(results)}건")
else:
    results = business_cards
    st.info(f"전체 명함: {len(results)}건")

# 결과 표시
st.markdown("---")
st.header("📇 담당자 정보")

if not results:
    st.warning("검색 결과가 없습니다.")
else:
    # 테이블 형식으로 표시
    table_data = []
    for card in results:
        table_data.append({
            "이름": card.get('name', 'N/A'),
            "기관": card.get('org', 'N/A'),
            "직책": card.get('position', 'N/A'),
            "연락처": card.get('contact', 'N/A'),
            "이력": card.get('history', 'N/A')
        })
    
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # 상세 카드 뷰
    st.markdown("---")
    st.subheader("📋 상세 정보")
    
    for i, card in enumerate(results, 1):
        with st.expander(f"💼 {i}. {card.get('name', 'N/A')} - {card.get('org', 'N/A')}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**이름:** {card.get('name', 'N/A')}")
                st.markdown(f"**기관:** {card.get('org', 'N/A')}")
                st.markdown(f"**직책:** {card.get('position', 'N/A')}")
            
            with col2:
                contact = card.get('contact', 'N/A')
                if contact and '@' in contact:
                    st.markdown(f"**이메일:** [{contact}](mailto:{contact})")
                else:
                    st.markdown(f"**연락처:** {contact}")
            
            st.markdown("---")
            st.markdown(f"**📝 이력:** {card.get('history', 'N/A')}")

# 기관별 통계
st.markdown("---")
st.header("📊 기관별 통계")

orgs = {}
for card in business_cards:
    org = card.get('org', '기타')
    if org not in orgs:
        orgs[org] = 0
    orgs[org] += 1

if orgs:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("기관별 담당자 수")
        for org, count in sorted(orgs.items(), key=lambda x: x[1], reverse=True):
            st.write(f"- **{org}**: {count}명")
    
    with col2:
        st.metric("전체 기관 수", len(orgs))
        st.metric("전체 담당자 수", len(business_cards))


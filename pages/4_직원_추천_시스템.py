"""
직원 추천 시스템 페이지
키워드 기반 직원 프로필 검색
"""

import streamlit as st
from utils.github_handler import load_data

st.set_page_config(
    page_title="직원 추천 시스템",
    page_icon="👥",
    layout="wide"
)

st.title("👥 직원 추천 시스템")

# 데이터 로드
staff_profiles = load_data("staff_profiles.json")

if not staff_profiles:
    st.error("❌ 데이터를 불러올 수 없습니다.")
    st.stop()

# 검색 기능
st.header("🔍 직원 검색")

search_keyword = st.text_input(
    "키워드를 입력하세요 (전문성, 관심사, 부서명 등)",
    placeholder="예: 학사관리, 데이터분석, 교학팀"
)

# 검색 함수
def search_staff(keyword: str, profiles: list) -> list:
    """키워드 기반 직원 검색"""
    if not keyword:
        return profiles
    
    keyword_lower = keyword.lower()
    results = []
    
    for profile in profiles:
        score = 0
        # 부서명 매칭
        if keyword_lower in profile.get("dept", "").lower():
            score += 10
        # 전문성 매칭
        for expertise in profile.get("expertise", []):
            if keyword_lower in expertise.lower():
                score += 8
        # 관심사 매칭
        for interest in profile.get("interests", []):
            if keyword_lower in interest.lower():
                score += 5
        # 이름 매칭
        if keyword_lower in profile.get("name", "").lower():
            score += 3
        
        if score > 0:
            results.append((profile, score))
    
    # 점수순 정렬
    results.sort(key=lambda x: x[1], reverse=True)
    return [r[0] for r in results]

# 검색 결과
if search_keyword:
    results = search_staff(search_keyword, staff_profiles)
    st.info(f"'{search_keyword}' 검색 결과: {len(results)}명")
else:
    results = staff_profiles
    st.info(f"전체 직원: {len(results)}명")

# 프로필 카드 표시
st.markdown("---")
st.header("👤 직원 프로필")

if not results:
    st.warning("검색 결과가 없습니다.")
else:
    # 2열 그리드로 표시
    cols = st.columns(2)
    
    for i, profile in enumerate(results):
        with cols[i % 2]:
            with st.container():
                st.markdown("---")
                st.subheader(f"👤 {profile.get('name', 'N/A')}")
                
                # 부서
                st.markdown(f"**부서:** {profile.get('dept', 'N/A')}")
                
                # 전문성 태그
                expertise = profile.get('expertise', [])
                if expertise:
                    st.markdown("**전문성:**")
                    tags = " ".join([f"`{e}`" for e in expertise])
                    st.markdown(tags)
                
                # 관심사 태그
                interests = profile.get('interests', [])
                if interests:
                    st.markdown("**관심사:**")
                    tags = " ".join([f"`{i}`" for i in interests])
                    st.markdown(tags)
                
                # 이메일
                email = profile.get('email', '')
                if email:
                    st.markdown(f"**이메일:** {email}")

# 부서별 필터
st.markdown("---")
st.header("📊 부서별 직원")

departments = sorted(list(set([p.get('dept') for p in staff_profiles if p.get('dept')])))

selected_dept = st.selectbox("부서를 선택하세요", ["전체"] + departments)

if selected_dept and selected_dept != "전체":
    dept_staff = [p for p in staff_profiles if p.get('dept') == selected_dept]
    st.info(f"{selected_dept} 소속 직원: {len(dept_staff)}명")
    
    for profile in dept_staff:
        with st.expander(f"👤 {profile.get('name', 'N/A')}"):
            st.write("**부서:**", profile.get('dept', 'N/A'))
            st.write("**전문성:**", ", ".join(profile.get('expertise', [])))
            st.write("**관심사:**", ", ".join(profile.get('interests', [])))
            st.write("**이메일:**", profile.get('email', 'N/A'))


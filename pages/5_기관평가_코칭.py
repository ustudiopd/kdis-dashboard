"""
기관평가 코칭 페이지
평가 항목별 가이드라인 및 전년도 피드백 제공
"""

import streamlit as st
from utils.github_handler import load_data

st.set_page_config(
    page_title="기관평가 코칭",
    page_icon="📋",
    layout="wide"
)

st.title("📋 기관평가 코칭")

# 데이터 로드
evaluation_manual = load_data("evaluation_manual.json")

if not evaluation_manual:
    st.error("❌ 데이터를 불러올 수 없습니다.")
    st.stop()

st.info("""
이 페이지에서는 기관평가 항목별 가이드라인과 전년도 피드백을 확인할 수 있습니다.
각 평가 항목을 선택하여 상세 정보를 확인하세요.
""")

# 카테고리별로 그룹화
categories = {}
for item in evaluation_manual:
    category = item.get('category', '기타')
    if category not in categories:
        categories[category] = []
    categories[category].append(item)

# 카테고리 선택
st.markdown("---")
st.header("📂 평가 카테고리")

selected_category = st.selectbox(
    "카테고리를 선택하세요",
    ["전체"] + sorted(categories.keys())
)

# 평가 항목 표시
st.markdown("---")

if selected_category == "전체":
    st.header("📋 전체 평가 항목")
    for category, items in sorted(categories.items()):
        st.subheader(f"📂 {category}")
        for item in items:
            with st.expander(f"📌 {item.get('criteria', 'N/A')}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 💡 가이드라인")
                    st.info(item.get('guide', '가이드라인이 없습니다.'))
                
                with col2:
                    st.markdown("### 📝 전년도 피드백")
                    st.warning(item.get('prev_feedback', '전년도 피드백이 없습니다.'))
                
                st.markdown(f"**카테고리:** {item.get('category', 'N/A')}")
else:
    st.header(f"📂 {selected_category}")
    items = categories[selected_category]
    
    for item in items:
        with st.container():
            st.markdown("---")
            st.subheader(f"📌 {item.get('criteria', 'N/A')}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 💡 가이드라인")
                st.info(item.get('guide', '가이드라인이 없습니다.'))
            
            with col2:
                st.markdown("#### 📝 전년도 피드백")
                st.warning(item.get('prev_feedback', '전년도 피드백이 없습니다.'))
            
            # 요약 정보
            st.markdown("---")
            col3, col4 = st.columns(2)
            with col3:
                st.metric("카테고리", item.get('category', 'N/A'))
            with col4:
                st.metric("평가 항목", item.get('criteria', 'N/A'))

# 통계 정보
st.markdown("---")
st.header("📊 평가 항목 통계")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("전체 항목 수", len(evaluation_manual))

with col2:
    st.metric("카테고리 수", len(categories))

with col3:
    total_feedback = sum(1 for item in evaluation_manual if item.get('prev_feedback'))
    st.metric("피드백 보유 항목", f"{total_feedback}/{len(evaluation_manual)}")

# 카테고리별 항목 수
st.markdown("---")
st.subheader("📈 카테고리별 항목 수")

category_counts = {cat: len(items) for cat, items in categories.items()}
for category, count in sorted(category_counts.items()):
    st.write(f"- **{category}**: {count}개 항목")


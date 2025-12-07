"""
주간보고 AI 챗봇 페이지
키워드 기반 주간보고서 검색
"""

import streamlit as st
from utils.github_handler import load_data
from datetime import datetime

st.set_page_config(
    page_title="주간보고 AI 챗봇",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 주간보고 AI 챗봇")

# 데이터 로드
weekly_reports = load_data("weekly_reports.json")

if not weekly_reports:
    st.error("❌ 데이터를 불러올 수 없습니다.")
    st.stop()

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요! 주간보고서에 대해 궁금한 것이 있으시면 물어보세요. 예: '최근 주간보고서 보여줘', '교학팀 보고서', '이슈가 있는 보고서'"
        }
    ]

# 키워드 매칭 함수
def search_reports(query: str, reports: list) -> list:
    """키워드 기반 보고서 검색"""
    query_lower = query.lower()
    results = []
    
    for report in reports:
        score = 0
        # 부서명 매칭
        if query_lower in report.get("department", "").lower():
            score += 10
        # 요약 내용 매칭
        if query_lower in report.get("summary", "").lower():
            score += 5
        # 이슈 매칭
        for issue in report.get("issues", []):
            if query_lower in issue.lower():
                score += 8
        
        if score > 0:
            results.append((report, score))
    
    # 점수순 정렬
    results.sort(key=lambda x: x[1], reverse=True)
    return [r[0] for r in results]

# 채팅 메시지 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
if prompt := st.chat_input("주간보고서에 대해 물어보세요..."):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 검색 수행
    results = search_reports(prompt, weekly_reports)
    
    # 응답 생성
    with st.chat_message("assistant"):
        if results:
            response = f"**{len(results)}개의 보고서를 찾았습니다:**\n\n"
            for i, report in enumerate(results[:5], 1):  # 최대 5개만 표시
                response += f"**{i}. {report.get('date', 'N/A')} - {report.get('department', 'N/A')}**\n"
                response += f"   {report.get('summary', '')}\n"
                if report.get('issues'):
                    response += f"   ⚠️ 이슈: {', '.join(report.get('issues', []))}\n"
                response += f"   🔗 [링크]({report.get('link', '#')})\n\n"
            st.markdown(response)
        else:
            st.markdown("검색 결과가 없습니다. 다른 키워드로 시도해보세요.")
            st.info("💡 팁: 부서명(교학팀, 대외협력팀 등), 날짜, 또는 '이슈' 등의 키워드를 사용해보세요.")
        
        # 응답을 세션에 추가
        st.session_state.messages.append({
            "role": "assistant",
            "content": response if results else "검색 결과가 없습니다."
        })

# 최근 보고서 목록
st.markdown("---")
st.header("📋 최근 주간보고서")

# 날짜순 정렬 (최신순)
sorted_reports = sorted(weekly_reports, key=lambda x: x.get('date', ''), reverse=True)

for report in sorted_reports[:5]:  # 최근 5개만 표시
    with st.expander(f"📅 {report.get('date', 'N/A')} - {report.get('department', 'N/A')}"):
        st.write("**요약:**", report.get('summary', ''))
        if report.get('issues'):
            st.warning(f"⚠️ 이슈: {', '.join(report.get('issues', []))}")
        if report.get('link'):
            st.markdown(f"🔗 [전체 보고서 보기]({report.get('link', '#')})")


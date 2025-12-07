"""
스마트 일정 관리 페이지
직원별 일정 및 공통 빈 시간 찾기
"""

import streamlit as st
import pandas as pd
from utils.github_handler import load_data
from datetime import datetime, timedelta
from collections import defaultdict

st.set_page_config(
    page_title="스마트 일정 관리",
    page_icon="📅",
    layout="wide"
)

st.title("📅 스마트 일정 관리")

# 데이터 로드
schedules = load_data("schedules.json")

if not schedules:
    st.error("❌ 데이터를 불러올 수 없습니다.")
    st.stop()

# 직원 목록 추출
staff_names = sorted(list(set([s.get('name') for s in schedules if s.get('name')])))

# 직원 선택
st.header("👥 직원 선택")
selected_staff = st.multiselect(
    "일정을 확인할 직원을 선택하세요 (복수 선택 가능)",
    staff_names,
    help="여러 명을 선택하면 공통 빈 시간을 찾아줍니다."
)

if not selected_staff:
    st.info("👆 직원을 선택해주세요.")
    st.stop()

# 선택된 직원의 일정 필터링
filtered_schedules = [s for s in schedules if s.get('name') in selected_staff]

# 날짜별로 그룹화
schedules_by_date = defaultdict(list)
for schedule in filtered_schedules:
    date = schedule.get('date')
    if date:
        schedules_by_date[date].append(schedule)

# 날짜 선택
st.markdown("---")
st.header("📆 날짜 선택")

available_dates = sorted(schedules_by_date.keys())
if not available_dates:
    st.warning("선택한 직원의 일정 데이터가 없습니다.")
    st.stop()

selected_date = st.selectbox(
    "날짜를 선택하세요",
    available_dates
)

# 선택된 날짜의 일정 표시
st.markdown("---")
st.header(f"📋 {selected_date} 일정")

date_schedules = schedules_by_date[selected_date]

# 시간대 정의 (9:00 ~ 17:00)
time_slots = [f"{h}:00" for h in range(9, 18)]

# 각 직원별 바쁜 시간대
staff_busy_times = {}
for schedule in date_schedules:
    name = schedule.get('name')
    busy_slots = schedule.get('time_slots', [])
    if name not in staff_busy_times:
        staff_busy_times[name] = set()
    staff_busy_times[name].update(busy_slots)

# 일정 테이블
schedule_data = []
for schedule in date_schedules:
    schedule_data.append({
        "직원": schedule.get('name'),
        "바쁜 시간대": ', '.join(schedule.get('time_slots', [])),
        "이벤트": schedule.get('event', '')
    })

if schedule_data:
    df = pd.DataFrame(schedule_data)
    st.dataframe(df, use_container_width=True)
else:
    st.info("해당 날짜에 일정이 없습니다.")

# 공통 빈 시간 찾기
st.markdown("---")
st.header("🕐 공통 빈 시간")

if len(selected_staff) > 1:
    # 모든 직원의 바쁜 시간대 합집합
    all_busy_times = set()
    for name in selected_staff:
        if name in staff_busy_times:
            all_busy_times.update(staff_busy_times[name])
    
    # 빈 시간대 계산
    free_times = [t for t in time_slots if t not in all_busy_times]
    
    if free_times:
        st.success(f"✅ **{len(free_times)}개의 공통 빈 시간대를 찾았습니다:**")
        
        # 시간대를 그룹으로 표시
        cols = st.columns(min(5, len(free_times)))
        for i, time_slot in enumerate(free_times):
            with cols[i % len(cols)]:
                st.metric("", time_slot)
    else:
        st.warning("⚠️ 공통 빈 시간이 없습니다. 모든 시간대가 예약되어 있습니다.")
else:
    # 단일 직원 선택 시
    if selected_staff[0] in staff_busy_times:
        busy_times = staff_busy_times[selected_staff[0]]
        free_times = [t for t in time_slots if t not in busy_times]
        
        if free_times:
            st.success(f"✅ **{selected_staff[0]}님의 빈 시간대:**")
            cols = st.columns(min(5, len(free_times)))
            for i, time_slot in enumerate(free_times):
                with cols[i % len(cols)]:
                    st.metric("", time_slot)
        else:
            st.info(f"{selected_staff[0]}님은 해당 날짜에 모든 시간대가 예약되어 있습니다.")
    else:
        st.info(f"{selected_staff[0]}님의 일정 데이터가 없습니다.")

# 전체 일정 캘린더 뷰
st.markdown("---")
st.header("📊 전체 일정 요약")

# 날짜별 통계
summary_data = []
for date in available_dates:
    date_schedules = schedules_by_date[date]
    total_busy_slots = sum(len(s.get('time_slots', [])) for s in date_schedules)
    summary_data.append({
        "날짜": date,
        "일정 수": len(date_schedules),
        "총 바쁜 시간대": total_busy_slots
    })

if summary_data:
    df_summary = pd.DataFrame(summary_data)
    st.dataframe(df_summary, use_container_width=True)


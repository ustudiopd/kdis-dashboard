import os
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

# 데이터 저장 폴더 생성 (절대 경로 처리)
data_dir = Path('data')
try:
    data_dir.mkdir(exist_ok=True)
except OSError as e:
    print(f"❌ 데이터 폴더 생성 실패: {e}")
    exit(1)

# 1. 통합 대시보드 데이터 (Dashboard)
dashboard_data: Dict[str, Any] = {
    "kpi": {"total_students": 320, "partners": 45, "employment_rate": 92.5},
    "students_by_region": [
        {"region": "Asia", "count": 150}, {"region": "Africa", "count": 80},
        {"region": "Europe", "count": 40}, {"region": "Americas", "count": 30}, {"region": "Others", "count": 20}
    ],
    "mou_partners": [
        {"name": "World Bank", "country": "USA", "year": 2023},
        {"name": "ADB", "country": "Philippines", "year": 2022},
        {"name": "KOICA", "country": "Korea", "year": 2021}
    ]
}

# 2. 주간보고서 데이터 (Weekly Reports)
weekly_reports: List[Dict[str, Any]] = []
base_date = datetime.now()
for i in range(5):
    date_str = (base_date - timedelta(weeks=i)).strftime("%Y-%m-%d")
    weekly_reports.append({
        "date": date_str,
        "department": random.choice(["교학팀", "대외협력팀", "기획팀", "총무팀"]),
        "summary": f"{date_str} 주간 업무 보고입니다. 주요 행사 및 일정 공유드립니다.",
        "issues": ["행사장 예약 중복 가능성 있음", "예산 승인 지연 우려"] if i % 2 == 0 else [],
        "link": f"https://kdischool.ac.kr/report/{date_str}"
    })

# 3. 일정 데이터 (Schedules)
schedules: List[Dict[str, Any]] = []
staff_names = ["김철수", "이영희", "박지민", "최현우"]
for name in staff_names:
    for i in range(5):
        schedules.append({
            "name": name,
            "date": (base_date + timedelta(days=i)).strftime("%Y-%m-%d"),
            "time_slots": [f"{h}:00" for h in range(9, 18) if random.random() > 0.5],  # Busy slots
            "event": "수업" if random.random() > 0.7 else "회의"
        })

# 4. 직원 프로필 (Staff Profiles)
staff_profiles: List[Dict[str, Any]] = [
    {"name": "김철수", "dept": "교학팀", "expertise": ["학사관리", "LMS"], "interests": ["생성형AI", "독서"], "email": "cs_kim@kdis.ac.kr"},
    {"name": "이영희", "dept": "대외협력팀", "expertise": ["국제행사", "통역"], "interests": ["여행", "영어"], "email": "yh_lee@kdis.ac.kr"},
    {"name": "박지민", "dept": "기획팀", "expertise": ["예산", "성과관리"], "interests": ["데이터분석", "테니스"], "email": "jm_park@kdis.ac.kr"}
]

# 5. 기관평가 매뉴얼 (Evaluation Manual)
evaluation_manual: List[Dict[str, Any]] = [
    {"category": "교육과정", "criteria": "전임교원 확보율", "guide": "전년도 대비 5% 상승 목표 필요", "prev_feedback": "교원 다양성 부족 지적"},
    {"category": "학생지원", "criteria": "장학금 지급률", "guide": "지급 기준의 투명성 확보 문서화 필요", "prev_feedback": "규정 명문화 미흡"}
]

# 6. 명함 데이터 (Business Cards)
business_cards: List[Dict[str, Any]] = [
    {"name": "John Doe", "org": "World Bank", "position": "Senior Specialist", "contact": "john@wb.org", "history": "2023 입학설명회 참석"},
    {"name": "Jane Smith", "org": "UNESCO", "position": "Director", "contact": "jane@unesco.org", "history": "2024 공동 세미나 논의 중"}
]

# 파일 저장 함수 (에러 처리 포함)
def save_json(filename: str, data: Any) -> None:
    """JSON 파일을 안전하게 저장합니다."""
    filepath = data_dir / filename
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"✅ {filename} 저장 완료")
    except (IOError, OSError) as e:
        print(f"❌ {filename} 저장 실패: {e}")
        raise

# 모든 파일 저장 시도
try:
    save_json('dashboard_data.json', dashboard_data)
    save_json('weekly_reports.json', weekly_reports)
    save_json('schedules.json', schedules)
    save_json('staff_profiles.json', staff_profiles)
    save_json('evaluation_manual.json', evaluation_manual)
    save_json('business_cards.json', business_cards)
    print("\n✅ 6개의 더미 데이터 파일이 'data/' 폴더에 생성되었습니다.")
except Exception as e:
    print(f"\n❌ 데이터 생성 중 오류 발생: {e}")
    exit(1)


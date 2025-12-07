# 시스템 아키텍처 및 패턴 (System Patterns)

## 1. 전체 아키텍처  
- **아키텍처 타입**: Monolithic (Streamlit Single Application)
- **구조**: 
  ```
  kdis-dashboard/
  ├── main.py              # 메인 진입점
  ├── pages/               # 기능별 페이지 (7개)
  │   ├── 0_Admin.py
  │   ├── 1_통합_대시보드.py
  │   ├── 2_주간보고_AI_챗봇.py
  │   ├── 3_스마트_일정_관리.py
  │   ├── 4_직원_추천_시스템.py
  │   ├── 5_기관평가_코칭.py
  │   └── 6_명함_공유_허브.py
  ├── utils/               # 유틸리티 모듈
  │   └── github_handler.py
  └── data/                # 로컬 데이터 저장소 (폴백용)
  ```
- **데이터 흐름**: 
  - GitHub Repository → `load_data()` → 페이지 표시
  - 사용자 입력 → `save_data()` → GitHub Repository

## 2. 주요 디자인 패턴  
- **Repository Pattern**: `utils/github_handler.py`에서 데이터 접근 로직 캡슐화
- **Facade Pattern**: `load_data()`, `save_data()` 함수로 복잡한 GitHub API 로직 숨김
- **Fallback Pattern**: GitHub 실패 시 로컬 데이터로 자동 전환
- **Session State Pattern**: 주간보고 챗봇에서 채팅 히스토리 관리

## 3. 코딩 컨벤션  
- **함수명**: `snake_case` (예: `load_data`, `save_data`)
- **변수명**: `snake_case` (예: `weekly_reports`, `staff_profiles`)
- **클래스명**: `PascalCase` (현재 클래스 사용 없음)
- **상수**: `UPPER_SNAKE_CASE` (예: `MAX_FILE_SIZE`, `MAX_RETRIES`)
- **타입 힌트**: 사용 (예: `def load_data(filename: str) -> Optional[Dict[str, Any]]`)
- **문서화**: Docstring 사용 (모든 함수에 설명 추가)

## 4. 에러 처리 패턴
- **일관된 에러 처리**: 모든 페이지에서 동일한 패턴
  ```python
  data = load_data("filename.json")
  if not data:
      st.error("❌ 데이터를 불러올 수 없습니다.")
      st.stop()
  ```
- **재시도 로직**: GitHub API 호출 시 최대 3회 재시도
- **사용자 피드백**: 명확한 에러 메시지 및 경고 표시

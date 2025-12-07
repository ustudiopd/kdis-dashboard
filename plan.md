# KDI 스마트 행정 플랫폼 개발 계획

## 1. 기능 개요  
- **목표**: GitHub를 DB처럼 활용하는 Streamlit 기반의 AI 스마트 행정 플랫폼 프로토타입 구현. 서버 비용 없이 데이터를 관리하고 팀원들과 공유할 수 있는 시스템 구축.
- **범위**: 
  - ✅ 더미 데이터 생성 스크립트
  - ✅ Streamlit 메인 앱 및 7개 페이지 (Admin + 6개 기능 페이지)
  - ✅ GitHub API 연동 모듈 (데이터 로드/저장)
  - ✅ 에러 처리 및 데이터 검증 로직
  - ✅ 프로젝트 설정 파일 (requirements.txt, .gitignore, secrets.toml.example)
  - ❌ 실제 AI 모델 연동 (현재는 키워드 매칭으로 구현)
  - ❌ 사용자 인증 시스템 (추후 추가 가능)

## 2. 기술 설계  
- **아키텍처**: 
  - Streamlit Multi-page App 구조
  - GitHub Repository를 데이터 저장소로 활용
  - 로컬 폴더(`data/`)를 폴백 저장소로 사용
  - 모듈화된 구조: `utils/` 폴더에 핵심 로직 분리

- **데이터 모델**: 
  - JSON 파일 기반 데이터 저장
  - 6개 데이터 파일: dashboard_data.json, weekly_reports.json, schedules.json, staff_profiles.json, evaluation_manual.json, business_cards.json
  - 각 파일은 배열 또는 객체 형태의 JSON 구조

- **API 명세**: 
  - GitHub API (PyGithub 라이브러리 사용)
  - `load_data(filename)`: GitHub에서 JSON 로드 (실패 시 로컬 폴백)
  - `save_data(filename, json_content)`: GitHub에 JSON 저장 (커밋 및 푸시)

## 3. 변경 파일 목록  

### 생성할 파일:
1. `generate_mock_data.py` - 더미 데이터 생성 스크립트
2. `main.py` - Streamlit 메인 진입점
3. `pages/0_Admin.py` - 데이터 관리 페이지
4. `pages/1_통합_대시보드.py` - 통합 대시보드 페이지
5. `pages/2_주간보고_AI_챗봇.py` - 주간보고 챗봇 페이지
6. `pages/3_스마트_일정_관리.py` - 일정 관리 페이지
7. `pages/4_직원_추천_시스템.py` - 직원 추천 페이지
8. `pages/5_기관평가_코칭.py` - 기관평가 페이지
9. `pages/6_명함_공유_허브.py` - 명함 공유 페이지
10. `utils/github_handler.py` - GitHub API 연동 모듈
11. `utils/__init__.py` - Python 패키지 초기화 파일
12. `requirements.txt` - Python 패키지 의존성
13. `.gitignore` - Git 무시 파일 목록
14. `.streamlit/secrets.toml.example` - Streamlit 설정 예시 파일

### 생성할 디렉토리:
- `pages/` - Streamlit 페이지 파일들
- `utils/` - 유틸리티 모듈
- `data/` - 로컬 JSON 파일 저장소 (generate_mock_data.py 실행 시 생성)
- `.streamlit/` - Streamlit 설정 폴더

## 4. 구현 단계 (Step-by-Step)  

### **1단계: 프로젝트 기본 구조 및 설정 파일 생성**
- `requirements.txt` 작성 (streamlit, pandas, plotly, PyGithub 등)
- `.gitignore` 작성 (secrets.toml, data/, __pycache__ 등 제외)
- `.streamlit/secrets.toml.example` 작성
- `utils/__init__.py` 생성

### **2단계: 더미 데이터 생성 스크립트 구현**
- `generate_mock_data.py` 작성 (제작.md의 코드 사용)
- 6개 JSON 파일 생성 로직 구현
- 에러 처리 및 타입 힌트 포함

### **3단계: GitHub 연동 모듈 구현**
- `utils/github_handler.py` 작성
- `load_data()` 함수: GitHub에서 JSON 로드, 실패 시 로컬 폴백
- `save_data()` 함수: GitHub에 JSON 저장 (커밋 및 푸시)
- 에러 처리: 재시도 로직(최대 3회), 타임아웃(30초), 명확한 에러 메시지
- 데이터 검증: JSON 형식 검증, 파일 크기 제한(10MB)

### **4단계: 메인 앱 및 사이드바 구현**
- `main.py` 작성
- 사이드바: 로고, 메뉴 네비게이션, 관리자 메뉴
- 페이지 라우팅 설정

### **5단계: Admin 페이지 구현**
- `pages/0_Admin.py` 작성
- 파일 업로더 구현
- JSON 미리보기 기능
- 파일 검증 (크기, 형식)
- GitHub 저장 기능 연동
- 성공/실패 피드백 메시지

### **6단계: 기능 페이지들 구현**
- `pages/1_통합_대시보드.py`: Plotly 차트 시각화 (Pie, Bar)
- `pages/2_주간보고_AI_챗봇.py`: 채팅 UI, 키워드 매칭 검색
- `pages/3_스마트_일정_관리.py`: 직원 선택, 공통 빈 시간 찾기
- `pages/4_직원_추천_시스템.py`: 키워드 검색, 프로필 카드 렌더링
- `pages/5_기관평가_코칭.py`: 평가 항목 선택, 가이드라인 출력
- `pages/6_명함_공유_허브.py`: 기관명 검색, 테이블 출력

### **7단계: 통합 테스트 및 최종 검증**
- 모든 페이지 동작 확인
- GitHub 연동 테스트 (로컬 폴백 포함)
- 에러 처리 시나리오 테스트
- 데이터 검증 로직 테스트

## 5. 테스트 계획  
- **단위 테스트**: 
  - `github_handler.py`의 `load_data()`, `save_data()` 함수 테스트
  - JSON 검증 로직 테스트
  - 에러 처리 로직 테스트

- **통합 테스트**: 
  - GitHub API 연동 → 로컬 폴백 시나리오
  - 파일 업로드 → 검증 → GitHub 저장 플로우
  - 각 페이지의 데이터 로드 및 표시

- **사용자 시나리오 테스트**: 
  1. 더미 데이터 생성 스크립트 실행
  2. Streamlit 앱 실행
  3. 각 페이지 접근 및 기능 사용
  4. Admin 페이지에서 파일 업로드 및 GitHub 저장
  5. GitHub에서 데이터 변경 후 앱에서 반영 확인

# 기술 스택 정보 (Tech Context)

## 1. 프레임워크 및 라이브러리  
- **언어 및 버전**: Python 3.12.10
- **핵심 프레임워크**: Streamlit 1.50.0 (Multi-page Application)
- **데이터베이스**: GitHub Repository (JSON 파일 기반)
- **상태 관리**: Streamlit Session State
- **UI 라이브러리**: Streamlit 기본 컴포넌트 + Tailwind CSS (CDN)
- **스타일링**: 
  - Tailwind CSS 3.x (CDN): 유틸리티 기반 CSS 프레임워크
  - Pretendard 폰트: 한글 가독성 최적화 폰트
  - 커스텀 CSS: KDI 브랜드 컬러 적용
- **주요 라이브러리**: 
  - `pandas` 2.3.3: 데이터 처리 및 테이블 표시
  - `plotly` 6.5.0: 인터랙티브 차트 시각화
  - `PyGithub` 2.8.1: GitHub API 연동
  - `python-dotenv` 1.0.0: 환경 변수 관리

## 2. 개발 환경  
- **패키지 매니저**: pip
- **Linter / Formatter**: 미설정 (기본 Python 스타일)
- **버전 관리**: Git
- **리포지토리**: GitHub (ustudiopd/kdis-dashboard)

## 3. 배포 환경  
- **호스팅**: Streamlit Cloud (예정) 또는 로컬 실행
- **CI/CD**: 미설정
- **데이터 저장소**: GitHub Repository (`data/` 폴더)
- **설정 관리**: Streamlit Secrets (`.streamlit/secrets.toml`)

## 4. 아키텍처 특징
- **데이터 저장 방식**: GitHub Repository를 DB처럼 활용
- **폴백 메커니즘**: GitHub 실패 시 로컬 `data/` 폴더에서 로드
- **에러 처리**: 재시도 로직 (최대 3회), 타임아웃 (30초)
- **데이터 검증**: JSON 형식 검증, 파일 크기 제한 (10MB)
- **스타일 시스템**: 
  - 모듈화된 스타일 로더 (`utils/style.py`)
  - Tailwind CSS CDN 주입 방식
  - KDI 브랜드 컬러 팔레트 (Forest Green #155e34, Charcoal #1f2937)
  - 재사용 가능한 컴포넌트 함수 (card_metric, page_header, badge)

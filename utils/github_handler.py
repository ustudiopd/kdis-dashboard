"""
GitHub API 연동 모듈
GitHub Repository를 데이터베이스처럼 활용하여 JSON 파일을 저장/로드합니다.
"""

import json
import streamlit as st
from pathlib import Path
from typing import Dict, Any, Optional
from github import Github
from github.GithubException import GithubException
import time

# 상수 정의
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_RETRIES = 3
TIMEOUT_SECONDS = 30


def _get_github_client() -> Optional[Github]:
    """GitHub 클라이언트를 생성합니다."""
    try:
        token = st.secrets.get("GITHUB_TOKEN")
        if not token:
            st.warning("⚠️ GitHub 토큰이 설정되지 않았습니다. 로컬 데이터를 사용합니다.")
            return None
        return Github(token, timeout=TIMEOUT_SECONDS)
    except Exception as e:
        st.warning(f"⚠️ GitHub 클라이언트 생성 실패: {e}. 로컬 데이터를 사용합니다.")
        return None


def _load_from_local(filename: str) -> Optional[Dict[str, Any]]:
    """로컬 파일에서 JSON 데이터를 로드합니다."""
    data_path = Path('data') / filename
    try:
        if data_path.exists():
            with open(data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    except (IOError, json.JSONDecodeError) as e:
        st.error(f"❌ 로컬 파일 로드 실패 ({filename}): {e}")
        return None


def load_data(filename: str) -> Optional[Dict[str, Any]]:
    """
    GitHub Repository에서 JSON 파일을 로드합니다.
    실패 시 로컬 data/ 폴더에서 로드합니다.
    
    Args:
        filename: 로드할 JSON 파일명 (예: 'dashboard_data.json')
        
    Returns:
        JSON 데이터 (dict) 또는 None
    """
    # GitHub에서 로드 시도
    github_client = _get_github_client()
    if github_client:
        try:
            repo_name = st.secrets.get("REPO_NAME")
            branch_name = st.secrets.get("BRANCH_NAME", "main")
            
            if not repo_name:
                st.warning("⚠️ GitHub 레포지토리 이름이 설정되지 않았습니다. 로컬 데이터를 사용합니다.")
                return _load_from_local(filename)
            
            repo = github_client.get_repo(repo_name)
            file_path = f"data/{filename}"
            
            # 재시도 로직
            for attempt in range(MAX_RETRIES):
                try:
                    file_content = repo.get_contents(file_path, ref=branch_name)
                    content = file_content.decoded_content.decode('utf-8')
                    data = json.loads(content)
                    return data
                except GithubException as e:
                    # 401 인증 오류 처리
                    if e.status == 401:
                        st.error("❌ GitHub 인증 오류: 토큰이 만료되었거나 유효하지 않습니다.")
                        st.info("""
                        **해결 방법:**
                        1. GitHub → Settings → Developer settings → Personal access tokens
                        2. 새 토큰 생성 (repo 권한)
                        3. `.streamlit/secrets.toml` 파일의 `GITHUB_TOKEN` 값을 업데이트
                        4. 앱을 재시작하세요
                        """)
                        break
                    elif attempt < MAX_RETRIES - 1:
                        time.sleep(1)  # 1초 대기 후 재시도
                        continue
                    else:
                        st.warning(f"⚠️ GitHub에서 파일을 로드할 수 없습니다 ({filename}): {e}. 로컬 데이터를 사용합니다.")
                        break
                except json.JSONDecodeError as e:
                    st.error(f"❌ JSON 파싱 오류 ({filename}): {e}")
                    return _load_from_local(filename)
        except GithubException as e:
            # 최상위 레벨 인증 오류 처리
            if e.status == 401:
                st.error("❌ GitHub 인증 오류: 토큰이 만료되었거나 유효하지 않습니다.")
                st.info("""
                **해결 방법:**
                1. GitHub → Settings → Developer settings → Personal access tokens
                2. 새 토큰 생성 (repo 권한)
                3. `.streamlit/secrets.toml` 파일의 `GITHUB_TOKEN` 값을 업데이트
                4. 앱을 재시작하세요
                """)
            else:
                st.warning(f"⚠️ GitHub 연동 오류: {e}. 로컬 데이터를 사용합니다.")
        except Exception as e:
            st.warning(f"⚠️ GitHub 연동 오류: {e}. 로컬 데이터를 사용합니다.")
    
    # 로컬 폴백
    return _load_from_local(filename)


def _validate_json_data(data: Dict[str, Any], filename: str) -> bool:
    """JSON 데이터를 검증합니다."""
    # 파일 크기 검증 (대략적)
    data_str = json.dumps(data)
    if len(data_str.encode('utf-8')) > MAX_FILE_SIZE:
        st.error(f"❌ 파일 크기가 너무 큽니다 (최대 {MAX_FILE_SIZE / 1024 / 1024}MB): {filename}")
        return False
    
    # JSON 형식 검증
    try:
        json.dumps(data)  # 직렬화 가능한지 확인
    except (TypeError, ValueError) as e:
        st.error(f"❌ JSON 형식 오류 ({filename}): {e}")
        return False
    
    return True


def save_data(filename: str, json_content: Dict[str, Any]) -> bool:
    """
    JSON 데이터를 GitHub Repository에 저장합니다.
    
    Args:
        filename: 저장할 JSON 파일명 (예: 'dashboard_data.json')
        json_content: 저장할 JSON 데이터 (dict)
        
    Returns:
        저장 성공 여부 (bool)
    """
    # 데이터 검증
    if not _validate_json_data(json_content, filename):
        return False
    
    # GitHub 클라이언트 확인
    github_client = _get_github_client()
    if not github_client:
        st.error("❌ GitHub 토큰이 설정되지 않아 저장할 수 없습니다.")
        return False
    
    try:
        repo_name = st.secrets.get("REPO_NAME")
        branch_name = st.secrets.get("BRANCH_NAME", "main")
        
        if not repo_name:
            st.error("❌ GitHub 레포지토리 이름이 설정되지 않았습니다.")
            return False
        
        repo = github_client.get_repo(repo_name)
        file_path = f"data/{filename}"
        content_str = json.dumps(json_content, ensure_ascii=False, indent=4)
        
        # 재시도 로직
        for attempt in range(MAX_RETRIES):
            try:
                # 기존 파일 확인
                try:
                    existing_file = repo.get_contents(file_path, ref=branch_name)
                    # 파일이 존재하면 업데이트
                    repo.update_file(
                        file_path,
                        f"Update {filename}",
                        content_str,
                        existing_file.sha,
                        branch=branch_name
                    )
                except GithubException:
                    # 파일이 없으면 생성
                    repo.create_file(
                        file_path,
                        f"Create {filename}",
                        content_str,
                        branch=branch_name
                    )
                
                # 로컬에도 저장 (폴백용)
                data_path = Path('data') / filename
                data_path.parent.mkdir(exist_ok=True)
                with open(data_path, 'w', encoding='utf-8') as f:
                    json.dump(json_content, f, ensure_ascii=False, indent=4)
                
                return True
                
            except GithubException as e:
                # 401 인증 오류 처리
                if e.status == 401:
                    st.error("❌ GitHub 인증 오류: 토큰이 만료되었거나 유효하지 않습니다.")
                    st.info("""
                    **해결 방법:**
                    1. GitHub → Settings → Developer settings → Personal access tokens
                    2. 새 토큰 생성 (repo 권한)
                    3. `.streamlit/secrets.toml` 파일의 `GITHUB_TOKEN` 값을 업데이트
                    4. 앱을 재시작하세요
                    """)
                    return False
                elif attempt < MAX_RETRIES - 1:
                    time.sleep(1)
                    continue
                else:
                    st.error(f"❌ GitHub 저장 실패 ({filename}): {e}")
                    return False
            except Exception as e:
                st.error(f"❌ 저장 중 오류 발생 ({filename}): {e}")
                return False
                
    except GithubException as e:
        # 최상위 레벨 인증 오류 처리
        if e.status == 401:
            st.error("❌ GitHub 인증 오류: 토큰이 만료되었거나 유효하지 않습니다.")
            st.info("""
            **해결 방법:**
            1. GitHub → Settings → Developer settings → Personal access tokens
            2. 새 토큰 생성 (repo 권한)
            3. `.streamlit/secrets.toml` 파일의 `GITHUB_TOKEN` 값을 업데이트
            4. 앱을 재시작하세요
            """)
        else:
            st.error(f"❌ GitHub 연동 오류: {e}")
        return False
    except Exception as e:
        st.error(f"❌ GitHub 연동 오류: {e}")
        return False


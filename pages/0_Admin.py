"""
Admin 페이지 - 데이터 관리
JSON 파일 업로드 및 GitHub 저장 기능
"""

import streamlit as st
import json
from pathlib import Path
from utils.github_handler import save_data, load_data

st.set_page_config(
    page_title="데이터 관리 - Admin",
    page_icon="🔧",
    layout="wide"
)

st.title("🔧 데이터 관리 (Admin)")

# 파일 크기 제한 (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024

# 파일 업로드 섹션
st.header("📤 JSON 파일 업로드")

uploaded_file = st.file_uploader(
    "JSON 파일을 선택하세요",
    type=['json'],
    help="최대 10MB까지 업로드 가능합니다."
)

if uploaded_file is not None:
    # 파일 크기 검증
    file_size = len(uploaded_file.getvalue())
    if file_size > MAX_FILE_SIZE:
        st.error(f"❌ 파일 크기가 너무 큽니다. (현재: {file_size / 1024 / 1024:.2f}MB, 최대: {MAX_FILE_SIZE / 1024 / 1024}MB)")
    else:
        try:
            # 파일 내용 읽기
            content = uploaded_file.read().decode('utf-8')
            data = json.loads(content)
            
            # 파일명 추출
            filename = uploaded_file.name
            
            # 미리보기 섹션
            st.success(f"✅ 파일 업로드 성공: {filename} ({file_size / 1024:.2f}KB)")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📄 파일 미리보기")
                st.json(data)
            
            with col2:
                st.subheader("📊 데이터 정보")
                st.metric("파일 크기", f"{file_size / 1024:.2f} KB")
                st.metric("데이터 타입", type(data).__name__)
                
                if isinstance(data, dict):
                    st.metric("키 개수", len(data))
                elif isinstance(data, list):
                    st.metric("항목 개수", len(data))
            
            # GitHub 저장 버튼
            st.markdown("---")
            st.subheader("💾 GitHub 저장")
            
            if st.button("🚀 GitHub에 저장하기", type="primary", use_container_width=True):
                with st.spinner("GitHub에 저장 중..."):
                    success = save_data(filename, data)
                    
                    if success:
                        st.success(f"✅ {filename} 파일이 GitHub에 성공적으로 저장되었습니다!")
                        st.balloons()
                    else:
                        st.error(f"❌ {filename} 파일 저장에 실패했습니다. 에러 메시지를 확인해주세요.")
            
        except json.JSONDecodeError as e:
            st.error(f"❌ JSON 형식 오류: {e}")
            st.info("올바른 JSON 형식인지 확인해주세요.")
        except Exception as e:
            st.error(f"❌ 파일 처리 중 오류 발생: {e}")

# 현재 데이터 파일 목록
st.markdown("---")
st.header("📁 현재 데이터 파일 목록")

data_files = [
    "dashboard_data.json",
    "weekly_reports.json",
    "schedules.json",
    "staff_profiles.json",
    "evaluation_manual.json",
    "business_cards.json"
]

for filename in data_files:
    with st.expander(f"📄 {filename}"):
        data = load_data(filename)
        if data:
            st.json(data)
        else:
            st.warning(f"⚠️ {filename} 파일을 찾을 수 없습니다.")


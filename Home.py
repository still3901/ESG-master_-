import streamlit as st
st.set_page_config(page_icon="💸", layout="wide")
import pandas as pd
import numpy as np
import os
from pykrx import stock
import warnings
import datetime as dt
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, add_page_title
import plotly.graph_objects as go
import yfinance as yf
import matplotlib.pyplot as plt
import base64
from fuzzywuzzy import process



# 초기 세션 상태 설정
def initialize_session_state():
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.df_0702 = pd.read_csv("df_0702.csv")  # CSV 파일 경로 업데이트

# 페이지 설정
add_page_title()

show_pages(
    [
        Page("Home.py", "Home", "🏠"),
        Page("pages/설문조사.py", "설문조사 페이지", "📊"),
        Page("pages/성향에 따른 ESG 기업 추천.py", "성향에 따른 ESG 기업 추천", "📊"),
        Page("pages/섹터별 ESG 기업 추천.py", "섹터별 ESG 기업 추천", "🏢"),
        Page("pages/기업 상세 정보 페이지.py", "기업 상세 정보 페이지", "📈"),
        Page("pages/시각장애인용 정보 페이지.py", "시각장애인용 정보 페이지", "📈")
    ]
)

DATA_PATH = "./"
SEED = 42

# CSV 데이터를 불러오는 함수 (캐싱)
@st.cache_data(ttl=900)
def load_csv(path):
    return pd.read_csv(path)

# 세션 상태 초기화
initialize_session_state()

# 설문조사 부분
st.title(":green[미래를 위한 가장 효과적인 투자] :sunglasses:")
st.subheader(":green[<ESG마스터> 는 ESG 데이터를 기반으로 최적의 금융 투자를 돕는 플랫폼 입니다.]")
# st.markdown("<hr>", unsafe_allow_html=True)  # 구분선 추가

# 로컬 이미지를 base64로 인코딩하는 함수
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# 배경 이미지 설정
img_base64 = get_base64_of_bin_file('배경이미지.jpg')
background_image_style = f"""
<style>
.stApp {{
    background: url("data:image/jpg;base64,{img_base64}") no-repeat center center fixed;
    background-size: cover;
    

}}
</style>
"""
st.markdown(background_image_style, unsafe_allow_html=True)

# main-content의 CSS를 별도로 정의
main_content_style = """
<style>
.main-content {
    background-color: rgba(255, 255, 255, 0.9); /* 흰색 배경과 90% 불투명도 설정 */
    padding: 20px;
    border-radius: 10px;
    margin: 30px auto; /* 가운데 정렬 및 상하 마진 추가 */
    max-width: 1200px; /* 최대 너비 설정 */
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* 그림자 추가 */
    text-align: left;
}
# .stButton > button {
#             background-color: #1B7841; /* 색상 */
#             border: 5px outset rgba(215, 255, 206, 0.8); /* 흐린 효과의 테두리 설정 */
#             color: white;
#             padding: 10px 20px;
#             text-align: center;
#             text-decoration: none;
#             display: inline-block;
#             font-size: 20px;
#             margin: 4px 4px;
#             cursor: pointer;
#             border-radius: 10px
        }
        .st.button:hover {
            opacity: 0.8;
        }
</style>
"""
st.markdown(main_content_style, unsafe_allow_html=True)


# 페이지 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'Home'
    
st.markdown("""
    <style>
    .vertical-line {
        border-left: 7px solid white; /* 세로선 두께와 색상 */
        height: 250px; /* 세로선 높이 */
    }
    </style>
    """, unsafe_allow_html=True)

# 메인 함수: 레이아웃 및 사용자 상호작용 처리
def main():

    col1,col2,col3 = st.columns([1,0.1,1])
    
    # ESG 성향 파악하기 섹션
    with col1:
        st.markdown("<h2 style='margin-bottom: 1px; margin-top: -20px; color: #FFFFFF; text-shadow: 0 0 5px #000000;'>ESG 투자 성향 파악하기</h2>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #FFFFFF; text-shadow: 0 0 5px #000000;'>ESG 투자 성향 파악을 통해 "
                "가장 적합한 ESG 기업을 추천받으세요.<br>"
                "지금 바로! 아래의 버튼을 눌러 설문조사를 시작해 보세요!!</h4>", unsafe_allow_html=True)
    
        if st.button("성향 파악하기", key="survey"):
            switch_page('설문조사 페이지')
            
    with col2:
        st.markdown('<div class="vertical-line"></div>', unsafe_allow_html=True)

    # CSS 스타일 설정
    vertical_line_style = """
    <style>
    .vertical-line {
        border-left: 3px solid white; /* 세로선 두께와 색상 */
        height: 250px; /* 세로선 높이 */
    }
    </style>
    """

    st.markdown(vertical_line_style, unsafe_allow_html=True)

        
        
    # 기업 상세 페이지 섹션
    with col3:
        st.markdown("<h2 style='margin-bottom: -35px; color: #FFFFFF; text-shadow: 0 0 5px #000000;'>기업 상세 페이지</h2>", unsafe_allow_html=True)

        # 기업 선택 자동완성 입력 창
        selected_company = st.text_input("", placeholder="종목명을 입력하세요", key="company_input")
        df = st.session_state.df_0702
        if selected_company:
            company_names = df['회사명'].str.lower().unique()  # 기업명을 소문자로 변환하여 비교
            matches = process.extract(selected_company.lower(), company_names, limit=11)
            filtered_matches = [match[0] for match in matches if match[1] >= 20 and match[0].lower().startswith(selected_company.lower())]

            if len(filtered_matches) == 1:
                selected_company = filtered_matches[0]

            selected_company = st.selectbox("", filtered_matches)
        
        if st.button("바로가기", key="detail") and selected_company:
            # 회사 이름을 세션 상태에 저장
            st.session_state.selected_company = selected_company.upper()
            switch_page('기업 상세 정보 페이지')



if __name__ == "__main__":
    main()

st.markdown("<hr>", unsafe_allow_html=True)  # 구분선 추가

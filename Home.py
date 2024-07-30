import streamlit as st
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
def add_page_title():
    st.set_page_config(page_icon="💸", layout="wide")
    
add_page_title()

show_pages(
    [
        Page("Home.py", "Home", "🏠"),
        Page("pages/설문조사.py", "설문조사 페이지", "📋"),
        Page("pages/성향에 따른 ESG 기업 추천.py", "성향에 따른 ESG 기업 추천", "📊"),
        Page("pages/섹터별 ESG 기업 추천.py", "섹터별 ESG 기업 추천", "🏢"),
        Page("pages/기업 상세 정보 페이지.py", "기업 상세 정보 페이지", "📈")
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

def esg_text():
    st.markdown('<h2 class="white-text">ESG 등급의 중요성에 대해 알아보세요.</h2>', unsafe_allow_html=True)

    if 'active_tab' not in st.session_state:
        st.session_state['active_tab'] = None

    def switch_tab(tab_index):
        st.session_state['active_tab'] = tab_index

    st.markdown("""
        <style>
        .white-text {
            color: white;
        }
        .stButton button {
            margin: 0.5em;
        }
        </style>
    """, unsafe_allow_html=True)

    tabs = ["ESG 등급의 중요성", "투자 유치와의 관계", "중소기업 및 스타트업의 혜택", "기업 이미지와 소비자 행동"]
    
    # 상단에 버튼을 배치합니다.
    col1, col2, col3, col4 = st.columns(4)
    if col1.button(tabs[0], key="tab0"):
        switch_tab(0)
    if col2.button(tabs[1], key="tab1"):
        switch_tab(1)
    if col3.button(tabs[2], key="tab2"):
        switch_tab(2)
    if col4.button(tabs[3], key="tab3"):
        switch_tab(3)

    active_tab = st.session_state['active_tab']
    
    if active_tab is not None:
        if active_tab == 0:
            st.markdown('<h2 class="white-text">ESG 등급의 개요</h2>', unsafe_allow_html=True)
            st.markdown('<h3 class="white-text">ESG 등급은 환경(Environmental), 사회(Social), 지배구조(Governance) 측면에서 기업의 성과를 평가하여 부여하는 등급으로, 기업의 지속 가능성을 판단하는 중요한 지표입니다.</h3>', unsafe_allow_html=True)

            st.markdown('<h2 class="white-text">종합 등급 체계</h2>', unsafe_allow_html=True)
            st.markdown('''
                <h3 class="white-text">
                종합 등급은 다음과 같이 구성됩니다<br><br>
                A+ (최우수)<br>
                A (우수)<br>
                B+ (양호)<br>
                B (보통)<br>
                C (미흡)<br>
                D (매우 미흡)
                </h3>
                ''', unsafe_allow_html=True)
        
        elif active_tab == 1:
            st.markdown('<h2 class="white-text">투자 유치와의 관계</h2>', unsafe_allow_html=True)
            st.markdown('<h3 class="white-text">종합 등급에서 B+ 이상의 등급을 받은 기업은 ESG 경영 실행 기업으로 인정되어 국민연금의 ESG 투자규모 384.1조원(직접운용 99.7조원, 위탁운용 284.4조원)에 해당하는 투자를 받을 수 있는 기본 요건을 충족하게 됩니다.<br><br> 등급이 높을수록 벤치마크 대비(최대 10배) 많은 투자를 받을 수 있는 기회가 확대됩니다. 반면, D등급을 받은 기업은 벤치마크를 초과해 편입하지 않도록 금지되어 있습니다.<br><br> 글로벌 대기업의 경우, 블랙록과 같은 외국 투자사들이 ESG 경영이 미흡한(C 이하) 기업에서 투자를 회수하고, ESG 경영이 우수한(A 이상) 기업에 투자하는 경향이 강해지고 있습니다.</h3>', unsafe_allow_html=True)

        elif active_tab == 2:
            st.markdown('<h2 class="white-text">중소기업 및 스타트업의 혜택</h2>', unsafe_allow_html=True)
            st.markdown('<h3 class="white-text">중소기업 및 스타트업에게도 ESG 등급 평가는 매우 중요합니다.<br><br> ESG 경영 확인서를 받은 기업은 KB국민은행에서 기준금리+가산금리(4.5%)로 최대 10억원까지 대출을 받을 수 있으며, 높은 등급을 받을수록 최대 1.4%의 추가 우대 금리를 적용받을 수 있습니다.<br><br> IBK 기업은행, 하나은행 등에서도 우대 대출을 받을 수 있으며, 대기업의 협력업체는 추가적인 우대금리 대출을 받을 수 있습니다. <br><br>대표적으로 SK그룹 협력업체의 경우 SK그룹과 국민은행이 공동 출자한 1.2조원 규모 내에서 무이자로 대출을 받을 수 있습니다.</h3>', unsafe_allow_html=True)

        elif active_tab == 3:
            st.markdown('<h2 class="white-text">기업 이미지와 소비자 행동</h2>', unsafe_allow_html=True)
            st.markdown('<h3 class="white-text">소비자들은 단순한 정량적 가치보다 정성적 가치, 즉 ESG를 더 중요하게 판단하여 소비하는 경향이 증가하고 있습니다. <br><br>ESG 등급이 높은 기업은 소비자들로부터 긍정적인 이미지와 신뢰를 얻을 수 있으며, 이는 매출 증가와 브랜드 가치를 높이는 데 기여합니다.</h3>', unsafe_allow_html=True)



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
        df = df[df['years'] == 2023]
        
        if selected_company:
            company_names = df['회사명'].str.lower().unique()  # 기업명을 소문자로 변환하여 비교
            matches = process.extract(selected_company.lower(), company_names, limit=11)
            filtered_matches = [match[0] for match in matches if match[1] >= 20 and match[0].lower().startswith(selected_company.lower())]
            
            if len(filtered_matches) == 1:
                selected_company = filtered_matches[0]
                st.session_state.selected_company = selected_company.upper()
                switch_page('기업 상세 정보 페이지')
                selected_company = filtered_matches[0]
            elif len(filtered_matches) > 1:
                filtered_matches.insert(0, "기업을 선택하세요")
                selected_company = st.selectbox("", filtered_matches)
                if selected_company != "기업을 선택하세요":
                    st.session_state.selected_company = selected_company.upper()
                    switch_page('기업 상세 정보 페이지')
            else:
                selected_company = None

    esg_text()
    
if __name__ == "__main__":
    main()

st.markdown("<hr>", unsafe_allow_html=True)  # 구분선 추가

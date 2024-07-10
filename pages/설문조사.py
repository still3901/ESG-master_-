import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# def switch_page(page_name):
#     st.experimental_set_query_params(page=page_name)

# CSS 스타일 적용
st.markdown("""
    <style>
        .survey-title {
            font-size: 36px;
            font-weight: bold;
            text-align: left; /* 왼쪽 정렬 */
            margin-bottom: 20px; /* 설명과의 간격 추가 */
        }
        .survey-subtitle {
            font-size: 22px;
            margin-top: 20px; /* 타이틀과의 간격 추가 */
            margin-bottom: 20px;
            text-align: left; /* 왼쪽 정렬 */
        }
        .option-box {
            padding: 20px;
            border: 2px solid #d3d3d3;
            margin-bottom: 20px;
            background-color: rgba(255, 255, 255, 0.1); /* 투명 배경 */
            border-radius: 10px; /* 원형 박스 스타일 */
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); /* 박스 귀속 느낌 */
        }
        .sector-box {
            padding: 10px;
            border: 1px solid #d3d3d3;
            margin-bottom: 10px;
            background-color: rgba(255, 255, 255, 0.1); /* 투명 배경 */
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); /* 박스 귀속 느낌 */
        }
        .sector-box label {
            display: block;
            margin-bottom: 5px;
        }
        .checkbox-label {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        .checkbox-label input {
            margin-right: 10px;
        }
        .radio-option {
            display: flex;
            align-items: center;
            margin-bottom: 20px; /* 간격 추가 */
            padding: 10px;
            border: 1px solid #d3d3d3;
            border-radius: 10px; /* 원형 박스 스타일 */
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); /* 박스 귀속 느낌 */
            background-color: rgba(255, 255, 255, 0.1); /* 투명 배경 */
        }
        .radio-option img {
            margin-left: 10px;
            width: 40px; /* 이미지 크기 */
            height: 40px; /* 이미지 크기 */
        }
        .result-button {
            display: flex;
            justify-content: center;
        }
        .stButton > button {
            background-color: #4CAF50; /* 녹색 */
            border: 5px outset rgba(215, 255, 206, 0.8); /* 흐린 효과의 테두리 설정 */
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 20px;
            margin: 4px 4px;
            cursor: pointer;
            border-radius: 10px
        }
        .st.button:hover {
            opacity: 0.8;
        }
    </style>
    """, unsafe_allow_html=True)


def display_survey_page():
    st.markdown('<div class="survey-title">설문조사</div>', unsafe_allow_html=True)
    st.markdown('<div class="survey-subtitle">설문조사에 응답하고 개인 투자 성향에 맞는 ESG 기업을 추천받으세요.</div>', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.5])  # 비율 조정

    with col1:
        st.markdown('<div class="option-box"><b>ESG 상품 종류</b>', unsafe_allow_html=True)
        choice1 = st.radio(
            "",
            [
                "🌱 ESG 등급이 꾸준히 좋은 기업",
                "📈 ESG 등급이 상승세인 기업",
                "🚀 ESG 등급이 다음년도에 급등 할 기업"
            ]
        )

    with col2:
        st.markdown('<div class="option-box"><b>선호하는 섹터를 선택하세요 (최대 3개)</b></div>', unsafe_allow_html=True)
        sectors = [
            "소재(Ma)", "커뮤니케이션(Co)", "임의소비재(Cd)", "필수소비재(Cs)", 
            "에너지(En)", "금융(Fn)", "헬스케어(He)", "산업(In)", 
            "부동산(Re)", "기술(Te)", "유틸리티(Ut)", "해당없음(NOT)"
        ]
        
        selected_sectors = []
        for sector in sectors:
            if st.checkbox(sector, key=sector):
                selected_sectors.append(sector)
                
        if len(selected_sectors) > 3:
            st.error("최대 3개의 섹터만 선택할 수 있습니다. 선택을 줄여주세요.")
            return

    if st.button("결과 보기") and len(selected_sectors) <= 3:
        st.session_state.choice1 = choice1
        st.session_state.selected_sectors = selected_sectors
        st.session_state.page = 'recommendation'
        switch_page('성향에 따른 ESG 기업 추천')
        st.experimental_rerun()

def main():
    if 'page' not in st.session_state:
        st.session_state.page = 'survey'
        st.session_state.choice1 = None
        st.session_state.selected_sectors = []

    display_survey_page()

if __name__ == "__main__":
    main()
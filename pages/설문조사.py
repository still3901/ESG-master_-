import streamlit as st
st.set_page_config(page_icon="💸", layout="wide")
from streamlit_extras.switch_page_button import switch_page
import glob

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
        # .stButton > button {
        #     background-color: #4CAF50; /* 녹색 */
        #     border: 5px outset rgba(215, 255, 206, 0.8); /* 흐린 효과의 테두리 설정 */
        #     color: white;
        #     padding: 10px 20px;
        #     text-align: center;
        #     text-decoration: none;
        #     display: inline-block;
        #     font-size: 20px;
        #     margin: 4px 4px;
        #     cursor: pointer;
        #     border-radius: 10px
        }
        .st.button:hover {
            opacity: 0.8;
        }
        .stRadio > div {
        gap: 40px;
        
    }
    </style>
    """, unsafe_allow_html=True)


def display_survey_page():
    st.markdown('<div class="survey-title">설문조사</div>', unsafe_allow_html=True)
    st.markdown('<div class="survey-subtitle">설문조사에 응답하고 개인 투자 성향에 맞는 ESG 기업을 추천받으세요.</div>', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    col1, col2= st.columns([1,3])  # 비율 조정

    with col1:
        st.markdown('<div class="option-box"><b>ESG 상품 종류</b>', unsafe_allow_html=True)
        
        choice1 = st.radio(
            "",
            [
                "🌱 ESG 정상급 수호자 - 매년 최상위 등급 유지",
                "📈 ESG 상승세 리더 - 지속적인 등급 향상 중",
                "🚀 ESG 대반전 예감 - 내년 급등 기대주",
                "💫 신흥 ESG 스타 - 단숨에 상위권 진입"
            ]
        )
    selected_sectors = []
    
    with col2:
        st.markdown('<div class="option-box"><b>선호하는 섹터를 선택하세요 (최대 3개)</b></div>', unsafe_allow_html=True)
        sectors_1 = [
            '건설', '금속', '금융', '기계', '기타금융', '기타서비스', '기타제조업',
       '농업, 임업 및 어업', '비금속', '서비스업'
        ]
        
                
        sectors_2 = [
            '섬유', '오락·문화', '운수', '유통업', '음식료품', '인프라','전기전자',
            '종이목재', '출판·매체복제', '통신업'
        ]
        
        
        sectors_3 = [
            '화학','헬스케어'
        ] 
        
        
        # 세 개의 열로 나누어 각 섹터를 배치합니다.
        col_a, col_b, col_c = st.columns(3)

        with col_a:
            for sector in sectors_1:
                if st.checkbox(sector, key=sector):
                    selected_sectors.append(sector)

        with col_b:
            for sector in sectors_2:
                if st.checkbox(sector, key=sector):
                    selected_sectors.append(sector)

        with col_c:
            for sector in sectors_3:
                if st.checkbox(sector, key=sector):
                    selected_sectors.append(sector)
        
         
    if len(selected_sectors) > 3:
            st.error("최대 3개의 섹터만 선택할 수 있습니다. 선택을 줄여주세요.")
            return

    if st.button("결과 보기") and len(selected_sectors) <= 3:
        st.session_state.choice1 = choice1
        st.session_state.selected_sectors = selected_sectors
        st.session_state.page = '성향에 따른 ESG 기업 추천'
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
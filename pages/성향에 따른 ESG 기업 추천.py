import streamlit as st
st.set_page_config(page_icon="💸", layout="wide")
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

def display_page():
    st.title("성향에 따른 ESG 기업 추천")
    st.subheader("2024년 예측한 ESG종합등급이 B+이상인 기업을 보여줍니다.")
    st.markdown("<br>", unsafe_allow_html=True)  # 구분선 추가
    choice1 = st.session_state.get('choice1', '선택되지 않음')
    selected_sectors = st.session_state.get('selected_sectors', [])
    
    st.write(f"선택한 ESG 상품 종류: {choice1}")
    st.write(f"선택한 섹터: {', '.join(selected_sectors)}")
    st.markdown("<hr>", unsafe_allow_html=True)  # 구분선 추가


def display_recommendation_page():
    # Query params에서 선택한 값 가져오기
    choice1 = st.session_state.get('choice1', '선택되지 않음')
    selected_sectors = st.session_state.get('selected_sectors', [])

    # 각 choice1 값에 따른 파일 경로 설정
    file_paths = {
        "🌱 ESG 정상급 수호자 - 매년 최상위 등급 유지": "1조_기업필터최종_ESG 정상급 수호자 - 매년 최상위 등급 유지_V001.csv",
        "📈 ESG 상승세 리더 - 지속적인 등급 향상 중": "1조_기업필터최종_ESG 상승세 리더 - 지속적인 등급 향상 중_V001.csv",
        "🚀 ESG 대반전 예감 - 내년 급등 기대주": "1조_기업필터최종_ESG 대반전 예감 - 내년 급등 기대주_V001.csv",
        "💫 신흥 ESG 스타 - 단숨에 상위권 진입": "1조_기업필터최종_신흥 ESG 스타 - 단숨에 상위권 진입_V001.csv"
    }

    # 선택된 choice1에 따른 파일 경로 가져오기
    file_path = file_paths.get(choice1, None)
    
    if file_path:
        try:
            df = pd.read_csv(file_path)
            df = df.drop(columns=['stock_code'])
            
            if selected_sectors:
                df = df[df['업종명'].isin(selected_sectors)]
                # 등급 데이터의 순서를 지정하여 Categorical 타입으로 변환
                rating_order = ['A+', 'A0', 'B+']
                df['2024년'] = pd.Categorical(df['2024년'], categories=rating_order, ordered=True)
                
                # 2024 컬럼을 기준으로 오름차순 정렬
                df = df.sort_values(by='2024년')
                
            st.dataframe(df)
        except FileNotFoundError:
            st.error(f"CSV 파일 '{file_path}'을 찾을 수 없습니다. 파일 경로를 확인해 주세요.")
    else:
        st.write("선택된 ESG 상품 종류가 없습니다.")

    col1, col2 = st.columns([2.5, 1])

    with col1:
        if st.button("설문조사 다시하기"):  # type: ignore
            switch_page('설문조사 페이지')

    with col2:
        if st.button("섹터별 ESG 기업 더보기"):  # type: ignore
            switch_page('섹터별 ESG 기업 추천')


if __name__ == "__main__":
    display_page()
    display_recommendation_page()
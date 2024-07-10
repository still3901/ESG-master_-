import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

def display_page():
    st.title("성향에 따른 ESG 기업 추천")
    choice1 = st.session_state.get('choice1', '선택되지 않음')
    selected_sectors = st.session_state.get('selected_sectors', [])
    
    st.write(f"선택한 ESG 상품 종류: {choice1}")
    st.write(f"선택한 섹터: {', '.join(selected_sectors)}")
    st.markdown("<hr>", unsafe_allow_html=True)  # 구분선 추가

def display_recommendation_page():
    # Query params에서 선택한 값 가져오기
    choice1 = st.query_params.get('choice1', [''])[0]
    selected_sectors = st.query_params.get('sectors', [])
    
    # 올바른 파일 경로로 수정
    file_path = "df_0702.csv"
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        st.error("CSV 파일을 찾을 수 없습니다. 파일 경로를 확인해 주세요.")
        return
    st.dataframe(df)

    col1, col2 = st.columns([2.5,1])

    with col1:
        if st.button("설문조사 다시하기"): # type: ignore
         switch_page('설문조사 페이지')
           
    with col2:
        if st.button("섹터별 ESG 기업 더보기"): # type: ignore
         switch_page('섹터별 ESG 기업 추천')


if __name__ == "__main__":
    display_page()
    display_recommendation_page()
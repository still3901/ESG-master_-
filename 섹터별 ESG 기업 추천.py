import streamlit as st
import pandas as pd
import plotly.express as px
import random
from streamlit_extras.switch_page_button import switch_page

# 페이지 설정: 넓은 레이아웃
st.set_page_config(layout="wide")

def display_title_and_description():
    # 페이지 제목 및 설명
    st.write("""
    # ESG 기업 추천 💹
    각 분야에서 ESG 성과가 우수한 기업, ESG 성장가능성이 있는 기업을 제시!
    """)
    st.markdown("<hr>", unsafe_allow_html=True)  # 구분선 추가

def display_search_all_companies(df_0702):
    # 전체 데이터를 대상으로 기업 검색 기능 추가
    st.header("기업을 검색하세요")
    search_query = st.text_input("기업명을 입력하세요")

    if search_query:
        df_search = df_0702[df_0702['회사명'].str.contains(search_query, case=False, na=False)]
        st.write(f"검색 결과: {len(df_search)}개 기업이 검색되었습니다.")
        st.dataframe(df_search)
        
        # 상세페이지 이동 버튼
        if st.button(f"{search_query} 상세페이지로 이동"):
            st.session_state["selected_company"] = search_query
            switch_page("기업 상세 정보 페이지")
        
        st.markdown("<hr>", unsafe_allow_html=True)  # 구분선 추가
        
        # 검색된 기업의 GICS_Sector 값 가져오기
        if not df_search.empty:
            first_result_sector = df_search.iloc[0]['GICS_Sector']
            st.session_state['selected_sector'] = first_result_sector
            
            # GICS_Sector가 변경될 수 있으므로, 섹터 데이터를 필터링합니다.
            display_sector_data(first_result_sector, df_0702, search_query)
    else:
        # 초기화
        if 'selected_sector' in st.session_state:
            del st.session_state['selected_sector']

def display_sector_buttons(sectors):
    # 섹터 선택 버튼
    selected_sector = st.session_state.get('selected_sector', None)
    cols = st.columns(len(sectors), gap="small")  # 균등한 열 분배 및 작은 간격
    
    for i, sector in enumerate(sectors):
        # 버튼의 스타일을 설정하여 크기를 동일하게 설정
        button_style = """
        <style>
        .stButton > button {
            width: 100%;
            height: 150%;
            box-sizing: border-box;
        }
        </style>
        """
        st.markdown(button_style, unsafe_allow_html=True)
        
        if cols[i].button(sector, use_container_width=True):
            selected_sector = sector
            st.session_state['selected_sector'] = selected_sector
    
    return selected_sector
    
def display_sector_data(selected_sector, df_0702, search_query=None):
    # 선택된 섹터에 따라 데이터를 필터링
    df_filtered = df_0702[df_0702['GICS_Sector'] == selected_sector]

    if search_query:
        df_filtered['priority'] = df_filtered['회사명'].apply(lambda x: 0 if search_query in x else 1)
        df_filtered = df_filtered.sort_values(by='priority').drop(columns=['priority'])

    st.subheader(f"{selected_sector} 섹터 기업 검색")
    
    # 필터링된 데이터 표시
    st.dataframe(df_filtered)
    
    st.markdown("<hr>", unsafe_allow_html=True)  # 구분선 추가
    display_esg_scores(df_0702, selected_sector)
    
def display_esg_scores(df_0702, selected_sector=None):
    # 등급을 숫자 값으로 매핑
    grade_mapping = {
        'A+': 4,
        'A': 4,
        'B+': 3,
        'B': 2,
        'C': 1,
        'D': 0
    }
    
    # 숫자 값으로 매핑된 종합등급 추가
    df_0702['종합등급_숫자'] = df_0702['종합등급'].map(grade_mapping)

    # 업종별 평균 ESG 등급 계산
    industries = ["소재(Ma)", "커뮤니케이션(Co)","임의소비재(Cd)","필수소비재(Cs)","에너지(En)","금융(Fn)"
                  ,"헬스케어(He)","산업(In)","부동산(Re)","기술(Te)","유틸리티(Ut)","해당없음(NOT)"]
    scores = df_0702[df_0702['GICS_Sector'].isin(industries)].groupby('GICS_Sector')['종합등급_숫자'].mean().reindex(industries).fillna(0)

    # 숫자 값을 다시 등급으로 매핑
    reverse_grade_mapping = {v: k for k, v in grade_mapping.items()}
    scores_labels = scores.map(reverse_grade_mapping)

    industry_df = pd.DataFrame({
        '업종': industries,
        '평균 ESG 등급': scores,
        '평균 ESG 등급(레이블)': scores_labels
    })

    # 강조 색상 설정
    industry_df['색상'] = ['orange' if industry == selected_sector else 'lightblue' for industry in industries]

    # 평균 ESG 등급 기준으로 데이터 정렬
    industry_df = industry_df.sort_values(by='평균 ESG 등급', ascending=False)

    st.header("업종별 평균 ESG등급")
    # 바 차트 생성
    fig = px.bar(industry_df, x='업종', y='평균 ESG 등급', text='평균 ESG 등급(레이블)')
    fig.update_traces(textposition='outside')
    
    # 색상 강조
    fig.update_traces(marker=dict(color=industry_df['색상']))

    # y축 레이블을 등급으로 표기
    fig.update_yaxes(
        tickmode='array',
        tickvals=[0, 1, 2, 3, 4],
        ticktext=['D', 'C', 'B', 'B+', 'A/A+']
    )
    
    st.plotly_chart(fig)


# def display_sorting_criteria():
#     # 기업 정렬 기준 설명
#     st.write("""
#     전년도 ESG에 비해 예측 ESG가 높은 걸 우선시 배치

#     만약, 전년도에 비해 ESG 등급이 오른 기업이 없다면 상단에는 ESG 등급이 높은 기업을 배치
#     """)

def main():
    display_title_and_description()
    
    if 'selected_sector' not in st.session_state:
        st.session_state['selected_sector'] = None

    # CSV 파일에서 데이터 로드
    DATA_PATH = "./"
    df_0702 = pd.read_csv(DATA_PATH + "df_0702.csv")
    
    # 전체 데이터를 대상으로 기업 검색 기능 표시
    display_search_all_companies(df_0702)
    
    # 기업명이 입력되지 않았을 때만 섹터 선택 기능 표시
    if 'selected_sector' not in st.session_state or st.session_state['selected_sector'] is None:
        st.header("섹터를 선택하세요")
        
        # 섹터 목록 생성
        sectors = df_0702['GICS_Sector'].unique()
        selected_sector = display_sector_buttons(sectors)

        # 섹터가 선택되었을 때만 다음 내용 표시
        if selected_sector:
            display_sector_data(selected_sector, df_0702, search_query=None)
            

if __name__ == "__main__":
    main()

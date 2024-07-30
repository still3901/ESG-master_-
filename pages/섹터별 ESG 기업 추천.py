import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import plotly.express as px
from streamlit_extras.switch_page_button import switch_page
import random
import plotly.graph_objects as go


def display_title_and_description():
    # 페이지 제목 및 설명
    st.write("""
    # ESG 기업 추천 💹
    ## 각 분야에서 ESG 성과가 우수한 기업, ESG 성장가능성이 있는 기업을 제시!
    """)

    st.markdown("<br>", unsafe_allow_html=True)
    choice1 = st.session_state.get('choice1', '선택되지 않음')
    selected_sectors = st.session_state.get('selected_sectors', [])
    
    st.write(f"선택한 ESG 상품 종류: {choice1}")
    st.write(f"선택한 섹터: {', '.join(selected_sectors)}")
    st.markdown("<hr>", unsafe_allow_html=True)  # 구분선 추가

def display_search_all_companies(df_0702):
    # 전체 데이터를 대상으로 기업 검색 기능 추가
    st.header("기업을 검색하세요")
    global search_query
    search_query = st.text_input("기업명을 입력하세요").upper()

    if search_query:
        df_search = df_0702[df_0702['회사명'].str.contains(search_query, case=False, na=False)]
        df_search=df_search[df_search['years']==2023]
        st.write(f"검색 결과: {len(df_search)}개 기업이 검색되었습니다.")
        st.dataframe(df_search)
        
        # 상세페이지 이동 버튼
        if st.button(f"{search_query} 상세페이지로 이동"):
            st.session_state["selected_company"] = search_query
            switch_page("기업 상세 정보 페이지")
            
        st.markdown("<hr>", unsafe_allow_html=True)  # 구분선 추가
        
        # 검색된 기업의 GICS_Sector 값 가져오기
        if not df_search.empty:
            first_result_sector = df_search.iloc[0]['업종명']
            st.session_state['selected_sector'] = first_result_sector
    else:
        # 초기화
        if 'selected_sector' in st.session_state:
            del st.session_state['selected_sector']

def display_sector_buttons(sectors):
    # 섹터 선택 버튼
    selected_sector = st.session_state.get('selected_sector', None)
    cols = st.columns(len(sectors), gap="small")  # 균등한 열 분배 및 작은 간격
    button_style = """
        <style>
        .stButton > button {
            width: 300%;
            height: 150%;
            box-sizing: border-box;
        }
        </style>
        """
    buttons_per_row = 9
    for i in range(0, len(sectors), buttons_per_row):
        cols = st.columns(buttons_per_row)
        for j, sector in enumerate(sectors[i:i+buttons_per_row]):
            if cols[j].button(sector, use_container_width=True):
                selected_sector = sector

                st.session_state['selected_sector'] = selected_sector
    return selected_sector

def display_sector_data(selected_sector, df_0702, search_query=None):
    # 선택된 섹터에 따라 데이터를 필터링
    df_filtered = df_0702[df_0702['업종명'] == selected_sector]
    
    if search_query:
        df_filtered['priority'] = df_filtered['회사명'].apply(lambda x: 0 if search_query in x else 1)
        df_filtered = df_filtered.sort_values(by='priority').drop(columns=['priority'])
    
    st.subheader(f"{selected_sector} 섹터 기업 검색")
    
    # 필터링된 데이터 표시
    st.dataframe(df_filtered)
    st.markdown("<hr>", unsafe_allow_html=True)  # 구분선 추가
    
    display_esg_scores(df_0702, selected_sector)

    
def display_esg_scores(df_0702, selected_sector):
    # 등급을 숫자 값으로 매핑
    grade_mapping = {
        'A+': 4,
        'A0': 3,
        'B+': 2,
        'B0': 1,
        'C': 1,
        'D': 1,
        'B0 이하(자격없음)':1,
        'B 이하(자격 없음)':1,
    }
    
    # 숫자 값으로 매핑된 종합등급 추가
    df_0702['종합등급_숫자'] = df_0702['종합등급'].map(grade_mapping)
    
    # 업종별 평균 ESG 등급 계산
    industries = ['건설', '금속', '금융', '기계', '기타금융', '기타서비스', '기타제조업', '농업, 임업 및 어업',
       '비금속', '서비스업', '섬유', '오락·문화', '운수', '유통업', '음식료품', '인프라', '전기전자',
       '종이목재', '출판·매체복제', '통신업', '헬스케어', '화학',]
    df_0702_2023=df_0702[df_0702['years']==2023]
    scores = df_0702_2023[df_0702_2023['업종명'].isin(industries)].groupby('업종명')['종합등급_숫자'].mean().reindex(industries).fillna(0)

    df_0702_com=df_0702[df_0702['회사명']==search_query]
    
    scores_com = df_0702_com[df_0702_com['업종명'].isin(industries)].groupby('업종명')['종합등급_숫자'].mean().reindex(industries).fillna(0)
    
    # 숫자 값을 다시 등급으로 매핑
    reverse_grade_mapping = {v: k for k, v in grade_mapping.items()}
    scores_labels = scores.map(reverse_grade_mapping)

    industry_df = pd.DataFrame({
        '업종': industries,
        '평균 ESG 등급': scores,
        '평균 ESG 등급(레이블)': scores_labels
    })
    
    scores_com = [max(score, 0) for score in scores_com]
    # print(scores_com)
    
    industry_df_2 = pd.DataFrame({
        '업종': industries,
        '평균 ESG 등급': scores_com,
        '평균 ESG 등급(레이블)': scores_labels
    })

    # 강조 색상 설정
    industry_df['색상'] = ['orange' if industry == selected_sector else 'lightblue' for industry in industries]

    # 평균 ESG 등급 기준으로 데이터 정렬
    industry_df = industry_df.sort_values(by='평균 ESG 등급', ascending=False)

    st.header("섹터별 평균 ESG등급")
    
    # 바 차트 생성
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=industry_df['업종'],
        y=industry_df['평균 ESG 등급'],
        text=industry_df['평균 ESG 등급(레이블)'],
        marker_color=industry_df['색상'],
        textposition='outside',
        
        name='평균 ESG 등급'
    ))
    
    
    company_name = search_query if search_query else "기업을 검색하세요"
    fig.add_trace(go.Bar(
        x=industry_df_2['업종'],
        y=industry_df_2['평균 ESG 등급'],
        text=industry_df_2['평균 ESG 등급(레이블)'],
        textposition='outside',
        marker_color="#EF553B",
        name=company_name
    ))
    
    fig.update_yaxes(
        tickmode='array',
        tickvals=[1, 2, 3],
        ticktext=['B', 'B+', 'A/A+']
    )
    
    st.plotly_chart(fig)


def main():
    display_title_and_description()
    
    if '업종명' not in st.session_state:
        st.session_state['업종명'] = None

    # CSV 파일에서 데이터 로드
    DATA_PATH = "./"
    df_0702 = pd.read_csv(DATA_PATH + "df_0702.csv")
    
    # 전체 데이터를 대상으로 기업 검색 기능 표시
    display_search_all_companies(df_0702)
    
    # 기업명이 입력되지 않았을 때만 섹터 선택 기능 표시
    if '업종명' not in st.session_state or st.session_state['업종명'] is None:
        st.header("섹터를 선택하세요")
        
        # 섹터 목록 생성
        sectors = df_0702['업종명'].unique()
        selected_sector = display_sector_buttons(sectors)

        df_0702_2023=df_0702[df_0702['years']==2023]
        df_0702_2023=df_0702_2023[['years','업종명','회사명','전년도ESG','종합등급','E_환경등급','S_사회등급','G_지배구조등급','성장성 등급','재무구조 등급']]
        
        def replace_value(x):
            if x == 'A':
                return 'A0'
            elif x == 'B':
                return 'B+'
            elif x == 'B 이하(자격 없음)':
                return 'B0 이하(자격없음)'
            else:
                return x

        # '업종명' 열에 함수 적용하여 값 변경
        df_0702_2023['종합등급'] = df_0702_2023['종합등급'].apply(replace_value)
        df_0702_2023=df_0702_2023.sort_values(by='종합등급')
        # 섹터가 선택되었을 때만 다음 내용 표시
        if selected_sector:
            display_sector_data(selected_sector, df_0702_2023, search_query=None)
            

if __name__ == "__main__":
    main()
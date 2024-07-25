import streamlit as st
st.set_page_config(page_icon="💸", layout="wide")
import pandas as pd
import plotly.graph_objects as go
import FinanceDataReader as fdr
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np

DATA_PATH = "./"
SEED = 42

# 데이터셋 불러오기
df = pd.read_csv("df_0702.csv")  # CSV 파일 경로 확인
df['stock_code'] = df['stock_code'].astype(str).str.zfill(6)

#주식 데이터 가져오기
def get_stock_data(ticker, start_date, end_date):
    try:
        data = fdr.DataReader(ticker, start=start_date, end=end_date)
        return data
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None


#스타차트 비교 그래프
def star_chart(filtered_df,company_name):
    
    com_2023 = filtered_df[['years', '재무구조 등급', '성장성 등급', 'G_지배구조등급', 'E_환경등급', 'S_사회등급']]
    com_2023 = com_2023[com_2023['years'] == 2023]
    com_2023 = com_2023.drop(columns=['years'])   
    
    sector_value = filtered_df.iloc[0]['업종명']
    df_sector = filtered_df[filtered_df['업종명'] == sector_value]
    columns_to_average = ['재무구조 등급', '성장성 등급', 'G_지배구조등급', 'E_환경등급', 'S_사회등급']
    mean_values = df_sector[columns_to_average].mean()
    radii_2 = mean_values
    radii_2 = [*radii_2, radii_2[0]]
    radii = com_2023.iloc[0].values
    radii = [*radii, radii[0]]
    labels = ['재무구조 등급', '성장성 등급', 'G_지배구조등급', 'E_환경등급', 'S_사회등급']
    labels = [*labels, labels[0]]
    
    label_loc = np.linspace(start=0, stop=2*np.pi, num=len(radii))
    
    fig2 = plt.figure(figsize=(3, 3)) # 그래프 크기 설정
    ax2 = fig2.add_subplot(111, polar=True)
    ax2.plot(label_loc, radii, label=company_name, linestyle='solid', color='orange')
    ax2.fill(label_loc, radii, color=(1.0, 0.784, 0.392), alpha=0.3)

    ax2.plot(label_loc, radii_2, label=sector_value+"평균ESG등급", linestyle='dashed', color='grey')
    ax2.fill(label_loc, radii_2, color=(0.706, 0.706, 0.706), alpha=0.3)      
    ax2.set_xticks(label_loc, labels=None)
    ax2.set_xticklabels(labels, fontsize=5)
    ax2.set_yticklabels([])
    ax2.legend(loc='upper right', bbox_to_anchor=(1.65, 1.1), fontsize='small')
    st.pyplot(fig2)


# ESG 등급 및 재무성과 변화 추이 그래프 그리기
def esg_grade_sales(filtered_df):
    # 2019년을 제외한 데이터 필터링
    filtered_df = filtered_df[filtered_df['years'] != 2019]

    fig, ax1 = plt.subplots(figsize=(10 ,6))

    # 전년도ESG를 숫자로 매핑
    esg_order = ['없음', 'D0', 'C0', 'B0', 'B+', 'A0', 'A+']  # 등급 순서를 수정
    esg_mapping = {grade: idx for idx, grade in enumerate(esg_order)}
    filtered_df['전년도ESG_숫자'] = filtered_df['전년도ESG'].map(esg_mapping)

    # 전년도ESG를 막대 차트로 그리기
    ax1.bar(filtered_df['years'], filtered_df['전년도ESG_숫자'], color='lightblue', alpha=0.6, label='ESG등급')
    ax1.set_xlabel('Years')
    ax1.set_ylabel('ESG등급', color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    ax1.set_xticks(filtered_df['years'].unique())
    ax1.set_xticklabels(filtered_df['years'].unique().astype(int))

    # y축 라벨 설정 (상위 등급이 나중에 오도록)
    ax1.set_yticks(range(len(esg_order)))
    ax1.set_yticklabels(esg_order)

    # 매출액, 영업이익, 자산총계를 꺾은선 차트로 그리기
    ax2 = ax1.twinx()
    ax2.plot(filtered_df['years'], filtered_df['매출액'], color='r', marker='o', label='매출액')
    ax2.plot(filtered_df['years'], filtered_df['영업이익'], color='g', marker='s', label='영업이익')
    ax2.plot(filtered_df['years'], filtered_df['자본총계'], color='m', marker='^', label='자본총계')
    ax2.set_ylabel('금액 (단위: 억 원)')
    ax2.tick_params(axis='y')

    # 제목과 범례 설정
    plt.title('ESG 등급 및 재무성과 변화 추이')
    fig.tight_layout()
    fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
    st.pyplot(fig)




# 메인 함수: 사용자 인터페이스 구성 및 데이터 가져오기
def main():
    # 세션 상태 초기화
    if 'selected_company' not in st.session_state:
        st.session_state['selected_company'] = ''
        
    # 사이드바 설정
    st.sidebar.title("Stock Chart")
    company_name = st.sidebar.text_input("종목명을 입력하세요:").upper()
    
    # 종목명을 입력할 때마다 세션 상태 업데이트
    if company_name and company_name != st.session_state['selected_company']:
        st.session_state['selected_company'] = company_name

    selected_company = st.session_state['selected_company']
    
    # 세션 상태에서 선택된 회사명을 가져옴
    if 'selected_company' in st.session_state:
        company_name = st.session_state["selected_company"].upper()

    if company_name:
        st.session_state["selected_company"] = company_name
        filtered_df = df[df['회사명'] == company_name]

        col1, col2 = st.columns([2, 1])
        with col1:
            st.title(":green[기업 포트폴리오] :sunglasses:")
            st.subheader(":green[곧 다가올 ESG 공시 의무화!]")
            st.subheader(":green[EGS 경영을 통해 재무적 성과를 낼 수 있습니다.]")

        with col2:
            filtered_df_2023 = filtered_df[filtered_df['years'] == 2023]
            
            if not filtered_df_2023.empty:
                grade = filtered_df_2023.iloc[0]['종합등급']
                st.markdown(
                f'<h2 style="margin-bottom: 5px; margin-right: 20px; color: #008100; text-align: center;">"{company_name}"의 2024년 ESG등급 예측!!</h2>',
                unsafe_allow_html=True)

                st.markdown(
                    '<div style="padding: 7px; background-color: #3DB7CC; border-radius: 0px; '
                    'text-align: center; width: 350px; margin-left: 100px; margin: 0 auto;">'
                        '<div style="border: 3px solid #FFFFFF; padding: 0px;">'
                            f'<h1 style="margin-top: 0px; font-size: 40px; color: #FFFFFF; margin-left: 10px;">{grade}</h1>'
                        '</div>'
                    '</div>',
                    unsafe_allow_html=True
                )
            else:
                st.write(f"{company_name} 회사의 2023년 데이터가 없습니다.")

        st.markdown("<hr>", unsafe_allow_html=True)  # 구분선 추가
        st.header(f"{company_name}의 ESG 정보")
        if not filtered_df.empty:
            st.write(filtered_df)
        else:
            st.write("해당 기업의 정보를 찾을 수 없습니다.")

        # 종목명을 티커로 변환하여 데이터 가져오기
        if '회사명' in df.columns:  # '회사명' 컬럼이 있는지 확인
            filtered_df = df[df['회사명'].str.upper() == company_name.upper()]

            if not filtered_df.empty:
                st.header(f"{company_name.upper()} 주가")
                ticker = filtered_df.iloc[0]['stock_code']  # 'stock_code' 컬럼에서 티커 가져오기
                star_2023=True
                
                if ticker:
                    # 시작 날짜와 종료 날짜 입력 받기
                    start_date = st.sidebar.date_input("시작 날짜: ", value=pd.to_datetime("2023-07-01"))
                    end_date = st.sidebar.date_input("종료 날짜: ", value=pd.to_datetime("2024-07-09"))

                    # 데이터 가져오기
                    data = get_stock_data(ticker, start_date, end_date)

                    if data is not None:
                        # 데이터프레임의 행 수를 입력받아 보여주는 영역
                        num_row = st.sidebar.number_input("Number of Rows", min_value=1, max_value=len(data), value=min(1, len(data)))
                        st.dataframe(data[-num_row:].reset_index().sort_index(ascending=False).set_index("Date"))

                        # 차트 타입 선택
                        chart_type = st.sidebar.radio("Select Chart Type", ("Line",))

                        # 차트 생성
                        if chart_type == "Line":
                            line = go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close')
                            fig = go.Figure(line)
                        else:
                            st.error("Invalid Chart Type Selected")

                        # 레이아웃 업데이트 및 차트 출력
                        fig.update_layout(title=f"{ticker} Stock {chart_type} Chart", xaxis_title="Date", yaxis_title="Price")
                        st.plotly_chart(fig)
                    else:
                        st.write(f"Error fetching data for {ticker}. Please check the ticker or try again later.")
                else:
                    st.write(f"종목명 '{company_name}'에 대한 티커를 찾을 수 없습니다.")
                
                st.markdown("<hr>", unsafe_allow_html=True)  # 구분선 추가
                
                # 비교 그래프
                st.title(f"{company_name}의 비교 그래프를 확인하세요")
                st.markdown("<br>", unsafe_allow_html=True)
                col1, col2 = st.columns(2)

                with col1:
                    if st.header("섹터 평균 ESG등급과의 비교"):
                        star_chart(filtered_df, company_name)

                with col2:
                    if st.header("ESG등급 및 재무성과 변화 추이"):
                        esg_grade_sales(filtered_df)
    else:
        st.title(":green[기업 포트폴리오] :sunglasses:")
        st.subheader(":green[곧 다가올 ESG 공시 의무화!]")
        st.subheader(":green[EGS 경영을 통해 재무적 성과를 낼 수 있습니다.]")
        st.markdown("<hr>", unsafe_allow_html=True)  # 구분선 추가

if __name__ == "__main__":
    main()

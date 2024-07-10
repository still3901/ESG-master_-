import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import FinanceDataReader as fdr

# 데이터셋 불러오기
df = pd.read_csv("df_0702.csv")  # CSV 파일 경로 확인
df['stock_code'] = df['stock_code'].astype(str).str.zfill(6)

# 페이지 제목 설정
st.title(":green[기업 포트폴리오] :sunglasses:")
st.subheader(":green[곧 다가올 ESG 공시 의무화!]")
st.subheader(":green[EGS 경영을 통해 재무적 성과를 낼 수 있습니다.]")
st.markdown("<hr>", unsafe_allow_html=True)  # 구분선 추가
        
# 주식 데이터 가져오기
def get_stock_data(ticker, start_date, end_date):
    try:
        data = fdr.DataReader(ticker, start=start_date, end=end_date)
        return data
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None

# 메인 함수: 사용자 인터페이스 구성 및 데이터 가져오기
def main():

    # 사이드바 설정
    st.sidebar.title("Stock Chart")
    company_name = st.sidebar.text_input("종목명을 입력하세요:")

    # 세션 상태에서 선택된 회사명을 가져옴
    if 'selected_company' in st.session_state:
        company_name = st.session_state["selected_company"]
        st.header(f"{company_name}의 ESG 정보")

        # 선택된 회사명으로 데이터 필터링
        company_data = df[df['회사명'] == company_name]

        if not company_data.empty:
            st.write(company_data)
        else:
            st.write("해당 기업의 정보를 찾을 수 없습니다.")
    else:
        if company_name:
            st.header(f"{company_name}의 ESG 정보")

            # 입력된 회사명으로 데이터 필터링
            company_data = df[df['회사명'] == company_name]

            if not company_data.empty:
                st.write(company_data)
            else:
                st.write("해당 기업의 정보를 찾을 수 없습니다.")
        else:
            st.subheader("종목명을 입력하세요")

    st.sidebar.text("종목명: " + company_name)
    

    # 종목명을 티커로 변환하여 데이터 가져오기
    if '회사명' in df.columns:  # '회사명' 컬럼이 있는지 확인
        # 종목명을 대문자로 변환
        company_name_upper = company_name.upper()
        
        filtered_df = df[df['회사명'].str.upper() == company_name_upper]
        
        if not filtered_df.empty:
            st.header(f"{company_name} 주가")
            ticker = filtered_df.iloc[0]['stock_code']  # 'stock_code' 컬럼에서 티커 가져오기

            if ticker:
                # 시작 날짜와 종료 날짜 입력 받기
                start_date = st.sidebar.date_input("시작 날짜: ", value=pd.to_datetime("2023-07-01"))
                end_date = st.sidebar.date_input("종료 날짜: ", value=pd.to_datetime("2024-07-09"))

                # 데이터 가져오기
                data = get_stock_data(ticker, start_date, end_date)

                if data is not None:
                    # 데이터프레임의 행 수를 입력받아 보여주는 영역
                    num_row = st.sidebar.number_input("Number of Rows", min_value=1, max_value=len(data), value=min(5, len(data)))
                    st.dataframe(data[-num_row:].reset_index().sort_index(ascending=False).set_index("Date"))

                    # 차트 타입 선택
                    chart_type = st.sidebar.radio("Select Chart Type", ("Candle_Stick", "Line"))

                    # 차트 생성
                    if chart_type == "Candle_Stick":
                        candlestick = go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'])
                        fig = go.Figure(candlestick)
                    elif chart_type == "Line":
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
    

if __name__ == "__main__":
    main()

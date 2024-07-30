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
import pyttsx3
import speech_recognition as sr

def read_text(text):
    # pyttsx3 초기화
    engine = pyttsx3.init()

    # Set properties (optional)
    engine.setProperty('rate', 150)    
    # 텍스트 읽기
    engine.say(text)
    
    # 대기(말하기가 끝날 때까지)
    engine.runAndWait()

# 예제 텍스트
text_to_read = "본인의 성향을 선택하세요 ,일번,  매년 최상위 등급 유지 ,이번, 지속적인 등급 향상 중인 주  ,삼번, 내년 급등 기대주 ,사번, 단숨에 상위권 진입"
# 텍스트 읽기 함수 호출
read_text(text_to_read)
df= pd.read_csv('df_0702.csv')
# 음성 인식기 생성
recognizer = sr.Recognizer()

# 마이크로부터 음성 입력 받기
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
df['종합등급_숫자'] = df['종합등급'].map(grade_mapping)


#pd.read_Csc 불러오면 일부데이터에대해서만
my_dict = {'1번': pd.read_csv("1정상급수호자.csv"),
                    '2번': pd.read_csv("2상승세리더.csv"),
                      '3번': pd.read_csv("3대반전예감.csv"),
                      '4번':pd.read_csv("4신흥ESG스타.csv")}


with sr.Microphone() as source:
    for i in range(3):
        print("말씀해주세요...")
        audio = recognizer.listen(source)

        try:
            # Google Web Speech API를 사용하여 음성 인식 시도
            text = recognizer.recognize_google(audio, language='ko-KR')
            print(text)

            if text in my_dict:
                df_num = my_dict[text]
                break
            else:
                read_text("잘 이해하지 못했어요, 다시 한번 말씀해주세요.")
                
        except:
            read_text("잘 이해하지 못했어요, 다시 한번 말씀해주세요.")
            read_text(text_to_read)
    else:
        read_text("세 번의 시도 후에도 이해하지 못했습니다. 다시 시도해주세요.")
        raise SystemExit


    for j in range(0,df_num.shape[0],5):
        print(df_num['회사명'].iloc[j:j+5].tolist())
        for i in range(j+1,j+1+5):
            try:
                
                read_text(f"{j+i}  {df_num['회사명'].iloc[i-1]} 예측 종합등급은 {df_num['2024년'].iloc[i-1]}입니다.")
            except:
                pass

        print("말씀하세요")
        audio = recognizer.listen(source)
        text = recognizer.recognize_google(audio, language='ko-KR')
        print("audio=",text)
        if text in (list(map(lambda x: f"{x}번", range(j, j + 5)))):
            read_text("네 알겠습니다.")
            break
        
    text=int(text.replace("번", ""))
    
    df_last=df_num.iloc[text-1]

    read_text(f"{df_last['회사명']}의 2022년 ESG등급은 {(df_last['2022년'])}2023년 ESG등급은 {df_last['2023년']}2024년 ESG등급은 {df_last['2024년']}입니다.")
    read_text(f"ESG등급을 상세히 보시려면 1번 끝내려면 2번을 말하세요")

    try:
        audio = recognizer.listen(source)
        text = recognizer.recognize_google(audio, language='ko-KR')
    except:
        text="2번"

    print("audio=",text)

    if text=="1번":
        read_text("네 알겠습니다.")
        read_text(f"{df_last['회사명']}의 사회_등급은 {(df_last['S_value_등급'])}환경_등급은 {df_last['E_value_등급']}지배구조_등급은 {df_last['G_value_등급']} 성장성_등급은 {df_last['성장성_value_등급']} 재무구조_등급은 {df_last['재무_value_등급']}입니다. 이용해 주셔서 대단히 감사합니다.")
    elif text=="2번":
        read_text("네 알겠습니다.")
    else:
        read_text("네 알겠습니다.")
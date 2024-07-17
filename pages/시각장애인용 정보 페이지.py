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
    
    # 텍스트 읽기
    engine.say(text)
    
    # 대기(말하기가 끝날 때까지)
    engine.runAndWait()

# 예제 텍스트
text_to_read = "본인의 성향을 선택하세요 ,일번,  매년 최상위 등급 유지 ,이번, 지속적인 등급 향상 중  ,삼번, 내년 급등 기대주 ,사번, 단숨에 상위권 진입"

# 텍스트 읽기 함수 호출
read_text(text_to_read)



# 음성 인식기 생성
recognizer = sr.Recognizer()

# 마이크로부터 음성 입력 받기

with sr.Microphone() as source:
    print("말씀해주세요...")
    audio = recognizer.listen(source)

    try:
        # Google Web Speech API를 사용하여 음성 인식 시도
        text = recognizer.recognize_google(audio, language='ko-KR')
        
        if text=="1번":
            print(text)
        elif text=="2번":
            print(text)
        elif text=="3번":
            print(text)
        elif text=="4번":
            print(text)
        
    except :
        read_text("잘 이해하지 못했어요")




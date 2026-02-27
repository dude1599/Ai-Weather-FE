from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
import requests
import os
from dotenv import load_dotenv

load_dotenv()
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
app = FastAPI()

# 1. 자바에서 보낼 데이터 구조 정의 (Pydantic 모델)
class WeatherRequest(BaseModel):
    lat: float
    lon: float
    current: Dict        
    forecast: List[Dict]

# .\venv\Scripts\activate
# uvicorn main:app --reload
@app.post("/api/ai-weather") # GET에서 POST로 변경, 
def get_nvidia_weather(request: WeatherRequest):
    print(f"\n[요청 수신] 위도:{request.lat}, 경도:{request.lon}")
    
    # 2. 예보 데이터를 AI가 이해하기 쉽게 텍스트로 가공
    forecast_text = ""
    for fcst in request.forecast[:6]: # 향후 6시간치만 사용
        forecast_text += f"- {fcst['time'][:2]}시: {fcst['temp']}도, {fcst['sky']}({fcst['pty']})\n"

    prompt = f"""당신은 전문 기상 분석가입니다. 아래 데이터를 바탕으로 다정하게 분석 조언을 작성하세요.
    
    [현재 실황] 
    기온: {request.current.get('temp')}도 / 날씨: {request.current.get('pty')} / 습도: {request.current.get('humidity')}%
    
    [향후 6시간 예보 정보]
    {forecast_text}
    
    [출력 규칙]
    1. 현재 상황, 미래 예보, 행동 지침의 순서로 답변해.
    2. 우산 언급 주의: 예보 데이터의 '강수 형태(PTY)'가 '비', '눈', '빗방울'일 때만 우산을 언급해. 
    3. 단순 '흐림'이나 '구름많음'일 때는 우산 대신 '하늘이 흐려지니 참고하라'는 식으로만 조언해줘.
    5. 120자 이내의 한국어만으로 답변해."""
    
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "meta/llama-3.1-70b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200,
        "temperature": 0.8
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        ai_message = response.json()["choices"][0]["message"]["content"].strip()
        print(f"AI 분석 성공: {ai_message}")
        
        return {"model": "NVIDIA Llama 3.1", "aiAdvice": ai_message}
        
    except Exception as e:
        print(f"에러 발생: {e}")
        return {"model": "Error", "aiAdvice": "AI 분석 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요."}
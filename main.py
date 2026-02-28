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

    prompt = f"""당신은 밝고 친절한 '기상 캐스터'입니다. 아래 데이터를 바탕으로 친구에게 이야기하듯 다정하고 생생한 날씨 소식을 전해주세요.
    
    [현재 실황] 
    기온: {request.current.get('temp')}도 / 날씨: {request.current.get('pty')} / 습도: {request.current.get('humidity')}%
    
    [향후 6시간 예보 정보]
    {forecast_text}
    
    [출력 규칙]
    1. 반드시 한글(Hangul)만 사용하고, 한자(Hanja)는 절대로 쓰지 마세요. (Strictly Use Hangul ONLY, NO Hanja)
    2. "안녕하세요! 기상 캐스터입니다" 같은 인사는 생략하고 바로 본론만 말하세요.
    3. '현재 상황 -> 미래 예보 -> 다정한 행동 지침' 순서로 120자 이내로 작성하세요.
    4. 말투는 "~해요", "~하세요" 같은 부드러운 구어체를 사용하세요. 
    5. 단순 '흐림'이나 '구름많음'일 때는 우산 대신 '하늘이 흐려지니 참고하라'는 식으로만 조언해줘."""
    
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "meta/llama-3.1-70b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200,
        "temperature": 0.7
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
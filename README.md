# AI Weather Analysis Engine (Python)
전달받은 실시간 기상 데이터를 바탕으로 **NVIDIA Llama 3.1 70B** 모델을 통해 사용자 맞춤형 기상 조언을 생성하는 API 서버입니다.

## 🛠 Tech Stack
- **Framework:** FastAPI
- **Model:** Meta Llama 3.1 70B Instruct (via NVIDIA API)
- **Library:** Pydantic, Requests, Python-dotenv
- **Language:** Python 3.9+

## Key Features
- **Data Processing:** 자바 백엔드로부터 수신한 위경도, 기상청 실황 및 예보 데이터 가공
- **AI Analytics:** 데이터 기반의 다정한 기상 분석 및 행동 지침 생성
- **Rule-based Output:** 100자 이내 한국어 답변 및 상황별(비, 눈, 맑음) 조언 최적화

## Setup
1. 가상환경 생성 및 활성화
2. `.env` 파일에 `NVIDIA_API_KEY` 설정

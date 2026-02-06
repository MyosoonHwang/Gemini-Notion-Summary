🚀 Gemini-Notion-Summary
Gemini API와 Notion API를 결합하여 공부한 내용을 자동으로 요약하고, 이미지(아키텍처, 도표 등)를 분석하여 노션 페이지 하단에 기록해 주는 스마트 학습 비서입니다.

🌟 주요 기능 (Features)
지능형 텍스트 요약: Gemini 모델을 사용하여 복습하기 좋게 핵심 내용을 구조화합니다.

멀티모달 이미지 분석: Pillow 라이브러리로 전처리된 이미지를 분석하여 네트워크 구성도나 시장 전망 도표의 핵심을 짚어줍니다.

자동 페이지 탐색: 매번 ID를 복사할 필요 없이, 가장 최근에 수정한 페이지를 자동으로 찾아 작업합니다.

노션 블록 최적화: 단순히 텍스트를 붙이는 것이 아니라 노션의 제목(#), 목록(*) 자료형으로 정교하게 변환하여 기록합니다.

🛠️ 기술 스택 (Tech Stack)
Language: Python 3.14+

AI Model: Google Gemini 1.5 Flash (안정성 및 무료 쿼터 최적화)

APIs: Notion API, Google GenAI API

Libraries: notion-client, google-genai, python-dotenv, Pillow, requests

⚡ Quick Start
1. 환경 설정 (Prerequisites)
Notion My Integrations에서 통합 토큰을 발급받으세요.

Google AI Studio에서 Gemini API Key를 발급받으세요.

2. 설치 및 실행 (Installation)
Bash
# 리포지토리 클론
git clone https://github.com/MyosoonHwang/Gemini-Notion-Summary.git
cd Gemini-Notion-Summary

# 필수 라이브러리 설치
pip install -r requirements.txt
3. 환경 변수 설정 (.env)
프로젝트 루트 폴더에 .env 파일을 생성하고 아래 양식을 채워주세요.

Plaintext
NOTION_TOKEN=your_notion_token_here
GEMINI_API_KEY=your_gemini_api_key_here
4. 실행 (Execution)
노션에서 공부한 내용을 작성하거나 이미지를 업로드한 후, 아래 명령어를 실행하세요.

Bash
python test_notion.py
📌 Usage Rules (형식 규칙)
본 프로젝트는 가독성을 위해 다음 마크다운 규칙을 엄격히 준수합니다:

#: 문서 대제목

##: 주제목

###: 소제목

*** **: 목록 기호

강조 표시(**): 노션 본연의 깔끔함을 위해 사용하지 않으며 대신 이모지를 활용합니다.

👨‍💻 Author
황우혁 (Hwang Woo Hyeok)

Soongsil University, Computer Science

Interested in Cloud Engineering (Azure, NHN Cloud) & Networking

GitHub: @MyosoonHwang
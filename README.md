# 🚀Gemini-Notion-Summary
Gemini API와 Notion API를 결합하여 공부한 내용을 자동으로 요약하고, 이미지(아키텍처, 도표 등)를 분석하여 노션 페이지 하단에 기록해 주는 스마트 학습 비서입니다.

<p align="center"> <img src="https://raw.githubusercontent.com/MyosoonHwang/Gemini-Notion-Summary/main/logo.png" width="600"> </p>

## 🌟 주요 기능 (Features)
지능형 학습 요약: Gemini 모델을 사용하여 복습하기 좋게 핵심 개념과 용어를 구조화합니다.

멀티모달 이미지 분석: Pillow 라이브러리로 전처리(대비/선명도 향상)된 이미지를 분석하여 네트워크 구성도나 시장 전망 도표의 핵심을 분석합니다.

자동 페이지 탐색: 사용자가 가장 최근에 수정한 페이지를 자동으로 찾아 요약본을 추가합니다.

노션 블록 최적화: Gemini의 응답을 노션의 제목(#), 목록(*) 등 공식 블록 데이터 구조로 변환하여 기록합니다.

## 🛠️ 기술 스택 (Tech Stack)
Language: Python 3.14+

AI Model: Google Gemini 1.5 Flash (안정성 및 무료 쿼터 최적화)

APIs: Notion API, Google GenAI API

Libraries: notion-client, google-genai, python-dotenv, Pillow, requests

# ⚡ Quick Start
### 1. 환경 설정 (Prerequisites)
Notion My Integrations에서 통합 토큰을 발급받으세요.

Google AI Studio에서 Gemini API Key를 발급받으세요.

### 2. 설치 및 실행 (Installation)
```Bash
# 리포지토리 클론
git clone https://github.com/MyosoonHwang/Gemini-Notion-Summary.git
cd Gemini-Notion-Summary
```
# 필수 라이브러리 설치
```Bash
pip install -r requirements.txt
```
### 3. 환경 변수 설정 (.env)
프로젝트 루트 폴더에 .env 파일을 생성하고 아래 양식을 채워주세요. (.gitignore가 설정되어 있어 실제 키는 업로드되지 않습니다.)

```Bash Plaintext
NOTION_TOKEN=your_notion_token_here
GEMINI_API_KEY=your_gemini_api_key_here
```
### 4. 실행 (Execution)
노션에서 공부한 내용을 작성하거나 이미지를 업로드한 후, 아래 명령어를 실행하세요.

```Bash
python test_notion.py
```
## 📌 Usage Rules (형식 규칙)
본 프로젝트는 가독성 높은 노션 정리를 위해 다음 규칙을 준수합니다:

#: 문서 대제목

##: 주제목

###: 소제목

*** **: 목록 기호

## 💡 / 📌 이모지: 강조 기호(**) 대신 이모지를 사용하여 가독성을 높입니다.

## 👨‍💻 Author
황우혁 (Hwang Woo Hyeok)

숭실대학교 컴퓨터학부 (Soongsil Univ. Computer Science)

Cloud Engineering & Networking Enthusiast (Azure, NHN Cloud)

GitHub: @MyosoonHwang
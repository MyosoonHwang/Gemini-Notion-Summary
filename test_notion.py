import os
import io  # 이미지 바이트 처리를 위해 필요
import requests
from dotenv import load_dotenv
from notion_client import Client
from google import genai
from google.genai import types
# --- PIL 라이브러리 추가 ---
from PIL import Image, ImageEnhance

# 1. 환경 변수 및 클라이언트 로드
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
notion = Client(auth=NOTION_TOKEN)
gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_latest_page_id():
    """사용자가 가장 최근에 편집한 페이지 ID를 자동으로 추출합니다."""
    search_results = notion.search(
        sort={"direction": "descending", "timestamp": "last_edited_time"},
        page_size=1
    ).get("results")
    return search_results[0]["id"] if search_results else None

def fetch_notion_content(page_id):
    """노션 페이지 내의 텍스트와 이미지 URL을 추출합니다."""
    content = {"text": "", "images": []}
    blocks = notion.blocks.children.list(block_id=page_id).get("results", [])
    for block in blocks:
        b_type = block.get("type")
        if b_type in ["paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item"]:
            rich_text = block[b_type].get("rich_text", [])
            content["text"] += "".join([t.get("plain_text", "") for t in rich_text]) + "\n"
        elif b_type == "image":
            image_info = block[b_type]
            if image_info.get("type") == "file":
                content["images"].append(image_info["file"]["url"])
            elif image_info.get("type") == "external":
                content["images"].append(image_info["external"]["url"])
    return content

def download_notion_image(image_url):
    """
    S3 서명된 URL은 추가 인증 헤더를 보내면 400 에러가 발생합니다.
    따라서 headers 없이 요청해야 합니다.
    """
    try:
        # headers={...} 부분을 삭제합니다.
        response = requests.get(image_url, timeout=10) 
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"이미지 다운로드 실패: {e}")
        return None

# --- [신규 추가] 이미지 전처리 함수 ---
def preprocess_image(image_bytes):
    """
    이미지 바이트를 받아 PIL로 선명도와 대비를 향상시킨 후 다시 바이트로 반환합니다.
    도표나 글자가 많은 이미지 분석 성능을 높이기 위함입니다.
    """
    try:
        # 바이트 스트림을 PIL 이미지 객체로 엽니다.
        img = Image.open(io.BytesIO(image_bytes))
        
        # 1단계: 이미지를 RGB 모드로 변환 (PNG 투명도 문제 등 방지)
        if img.mode in ('RGBA', 'P'):
             img = img.convert('RGB')

        # 2단계: 대비(Contrast) 향상 (1.5배) -> 글자와 배경 구분 명확화
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.5)
        
        # 3단계: 선명도(Sharpness) 향상 (2.0배) -> 흐릿한 글자 선명하게
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(2.0)

        # 4단계: 처리된 이미지를 다시 바이트 스트림으로 저장 (JPEG 형식)
        output_buffer = io.BytesIO()
        img.save(output_buffer, format='JPEG', quality=95)
        processed_bytes = output_buffer.getvalue()
        
        print("⚡ 이미지 전처리(대비/선명도 향상) 완료")
        return processed_bytes
    except Exception as e:
        print(f"이미지 전처리 실패: {e}")
        # 전처리 실패 시 원본 데이터를 그대로 반환
        return image_bytes

def convert_to_notion_blocks(ai_text):
    """Gemini의 응답(마크다운)을 노션의 공식 블록 데이터 구조로 변환합니다."""
    blocks = []
    for line in ai_text.split('\n'):
        line = line.strip().replace("**", "")
        if not line: continue
        if line.startswith('### '):
            blocks.append({"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"text": {"content": line[4:]}}]}})
        elif line.startswith('## '):
            blocks.append({"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": line[3:]}}]}})
        elif line.startswith('# '):
            blocks.append({"object": "block", "type": "heading_1", "heading_1": {"rich_text": [{"text": {"content": line[2:]}}]}})
        elif line.startswith('* '):
            blocks.append({"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": line[2:]}}]}})
        else:
            blocks.append({"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": line}}]}})
    return blocks

# --- 핵심 프로세스 ---
target_id = get_latest_page_id()

if target_id:
    print(f"🚀 최신 페이지 탐색 완료 (ID: {target_id})")
    page_content = fetch_notion_content(target_id)
    
    prompt_text = f"""
    당신은 컴퓨터공학 전공생의 '스마트 학습 조언자'입니다. 
    제공된 [본문 내용]과 [이미지]를 공부하기 좋게 정리해 주세요.

    [정리 가이드]
    1. 복습하기 좋게 핵심 개념과 용어를 중심으로 정리하세요.
    2. 중요한 내용 앞에는 💡 또는 📌 이모지를 붙여서 강조해 주세요.
    3. 이미지가 있다면, "이 그림에서 꼭 기억해야 할 포인트"를 2~3가지 핵심만 짚어주세요.
    4. 전체 내용을 관통하는 '오늘의 한 줄 핵심'을 가장 마지막에 넣어주세요.

    [형식 규칙 - 절대 준수]
    - 강조를 위한 별표(**) 기호는 어떤 경우에도 사용하지 않습니다.
    - 제목은 #, 주제목은 ##, 소제목은 ### 형식을 사용합니다.
    - 목록은 * 기호만 사용합니다.
    {page_content['text']}
    """
    
    gemini_contents = [prompt_text]
    
    for img_url in page_content["images"]:
        raw_img_data = download_notion_image(img_url)
        if raw_img_data:
            # [변경] 다운로드한 이미지를 전처리 함수에 통과시킴
            processed_data = preprocess_image(raw_img_data)
            # 전처리된 데이터를 Gemini에게 전달 (MIME 타입은 JPEG로 통일)
            gemini_contents.append(
                types.Part(
                    inline_data=types.Blob(data=processed_data, mime_type="image/jpeg")
    )
)
            print("📸 이미지 데이터 로드 및 전처리 완료")

    print(f"🤖 Gemini 3.0 Pro 분석 시작...")
    response = gemini.models.generate_content(
        model="gemini-1.5-flash", # 복잡한 추론에 강한 Pro 모델 권장
        contents=gemini_contents
    )
    
    new_blocks = convert_to_notion_blocks(response.text)
    notion.blocks.children.append(block_id=target_id, children=new_blocks)
    
    print("✨ 텍스트 요약 및 이미지 정밀 분석 결과가 기록되었습니다!")
else:
    print("수정된 페이지를 찾을 수 없습니다.")
import openai
from typing import List
import base64
import os

def encode_image_to_base64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("utf-8")

def parse_cbt_problems_from_images(images: List[bytes]) -> List[dict]:
    openai.api_key = os.getenv("OPENAI_API_KEY")

    image_messages = [
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{encode_image_to_base64(img)}",
                "detail": "high"
            }
        } for img in images
    ]

    prompt = """以下の画像には歯科医師国家試験CBTの問題が複数含まれています。
各問題について次の形式のJSONで出力してください（リスト形式）：

[
  {
    "問題番号": "117A38",
    "問題文": "...",
    "選択肢": {
      "a": "...",
      "b": "...",
      "c": "...",
      "d": "...",
      "e": "..."
    },
    "正解": ["a"],
    "解説": "...",
    "教科分類": "歯科矯正学"
  }
]
出力はJSONのみにしてください。
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": [{"type": "text", "text": prompt}] + image_messages}
            ],
            temperature=0.2
        )
        content = response.choices[0].message["content"]
        json_start = content.find("[")
        json_text = content[json_start:]
        return eval(json_text)
    except Exception as e:
        return [{"エラー": str(e)}]
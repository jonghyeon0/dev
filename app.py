import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Render에서는 환경변수로 키를 관리합니다 (보안)
GOOGLE_API_KEY = os.environ.get('GEMINI_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# 시스템 프롬프트 (리더님의 비전)
SYSTEM_PROMPT = """
당신은 '일학OS: INTUITION 3.0'의 핵심 분석 엔진입니다.
(중략... 아까 작성한 HCI 프롬프트 내용 전체)
"""

model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=SYSTEM_PROMPT)

@app.route('/')
def home():
    return "일학OS 서버 정상 가동 중 (Render)"

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        url = data.get('url')
        response = model.generate_content(url)
        return jsonify({"result": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

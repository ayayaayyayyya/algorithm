import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # 앱스 스크립트에서 보낸 JSON 데이터 받기
        data = request.get_json(silent=True)
        print("받은 데이터:", data)
        
        # 정상적으로 받았다는 응답 반환
        return jsonify({
            "status": "success",
            "message": "데이터를 잘 받았어!",
            "received_data": data
        }), 200
        
    # GET 요청으로 접속했을 때
    return "on time", 200

if __name__ == "__main__":
    # Cloud Run이 주입하는 PORT 환경변수 사용 (기본값 8080)
    port = int(os.environ.get("PORT", 8080))
    # host='0.0.0.0' 바인딩이 핵심입니다!
    app.run(host="0.0.0.0", port=port)

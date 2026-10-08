import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Server is running!"

if __name__ == "__main__":
    # Cloud Run이 주입하는 PORT 환경변수 사용 (기본값 8080)
    port = int(os.environ.get("PORT", 8080))
    # host='0.0.0.0' 바인딩이 핵심입니다!
    app.run(host="0.0.0.0", port=port)

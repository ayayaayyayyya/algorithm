import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    # Cloud Run이 부여하는 PORT 환경 변수를 읽고, 없을 경우 기본값 8080 사용
    port = int(os.environ.get("PORT", 8080))
    # host='0.0.0.0' 바인딩 필수 (127.0.0.1이나 localhost는 접근 불가)
    app.run(host="0.0.0.0", port=port)

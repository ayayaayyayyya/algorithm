import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# 6주차 강의 내용: 버블 정렬 함수 (조기 종료 기법 적용)
def bubble_sort(arr):
    n = len(arr)
    arr = arr.copy()  # 원본 리스트 보존
    for i in range(n):
        swapped = False
        for j in range(0, n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        # 더 이상 교환이 일어나지 않으면 조기 종료 (최선 $O(N)$)
        if not swapped:
            break
    return arr

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # 앱스 스크립트에서 보낸 JSON 데이터 받기
        data = request.get_json(silent=True) or {}
        print("받은 데이터:", data)
        
        # 1. 정렬할 숫자 리스트 추출
        numbers = data.get("numbers")
        
        # 2. 예외 처리: numbers 데이터가 없거나 리스트가 아닌 경우
        if numbers is None or not isinstance(numbers, list):
            return jsonify({
                "status": "error",
                "message": "'numbers' 배열 데이터가 올바르게 전달되지 않았습니다."
            }), 400

        # 3. 버블 정렬 수행
        sorted_numbers = bubble_sort(numbers)
        
        # 4. 정렬 결과 반환
        return jsonify({
            "status": "success",
            "message": "버블 정렬이 성공적으로 완료되었습니다.",
            "original": numbers,
            "result": sorted_numbers
        }), 200
        
    # GET 요청으로 접속했을 때
    return "Cloud Run Algorithm Service is Running", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

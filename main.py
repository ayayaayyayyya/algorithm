import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# 고정 길이 원형 큐 (Fixed-Size Circular Queue) 클래스 구현
class FixedSizeQueue:
    def __init__(self, capacity=20):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front_idx = 0
        self.rear_idx = 0
        self.count = 0

    # 1. 초기화
    def init(self, capacity):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front_idx = 0
        self.rear_idx = 0
        self.count = 0

    # 4. 상태 검사 (empty)
    def is_empty(self):
        return self.count == 0

    # 4. 상태 검사 (full)
    def is_full(self):
        return self.count == self.capacity

    # 2. Push 동작
    def push(self, data):
        if self.is_full():
            return False, "큐가 가득 찼습니다 (Full)"
        self.queue[self.rear_idx] = data
        self.rear_idx = (self.rear_idx + 1) % self.capacity
        self.count += 1
        return True, "Push 성공"

    # 2. Pop 동작
    def pop(self):
        if self.is_empty():
            return False, "큐가 비어 있습니다 (Empty)"
        data = self.queue[self.front_idx]
        self.queue[self.front_idx] = None
        self.front_idx = (self.front_idx + 1) % self.capacity
        self.count -= 1
        return True, data

    # 3. 현재 데이터 개수(길이/크기) 반환
    def get_size(self):
        return self.count

    # 5. 전면(Front) 데이터 확인
    def get_front(self):
        if self.is_empty():
            return False, "큐가 비어 있습니다"
        return True, self.queue[self.front_idx]

    # 6. 큐 전체 데이터 삭제
    def clear(self):
        self.init(self.capacity)

    # 10. Front부터 Rear까지 출력하기 위해 데이터를 리스트로 변환
    def get_elements(self):
        elements = []
        for i in range(self.count):
            idx = (self.front_idx + i) % self.capacity
            elements.append(self.queue[idx])
        return elements

    # 7. 값의 index 검색 (Front 기준 0부터 시작)
    def index_of(self, value):
        elements = self.get_elements()
        if value in elements:
            return True, elements.index(value)
        return False, -1

    # 8. 값의 개수
    def count_of(self, value):
        return self.get_elements().count(value)

    # 9. 값의 존재 여부 검사
    def exists(self, value):
        return value in self.get_elements()


# 전역 큐 인스턴스 생성 (초기 사이즈 20)
q = FixedSizeQueue(20)


@app.route("/", methods=["GET"])
def health_check():
    return "Fixed-Size Queue Server is Running", 200


@app.route("/queue", methods=["POST"])
def manage_queue():
    data = request.get_json(silent=True) or {}
    action = data.get("action")
    
    response = {"status": "success", "action": action}

    # 1) 초기화
    if action == "init":
        cap = data.get("capacity", 20)
        q.init(cap)
        response["message"] = f"크기 {cap}인 큐로 초기화 되었습니다."
        
    # 2) Push
    elif action == "push":
        values = data.get("values", [])
        if isinstance(values, list): # 다중 Push 처리
            pushed = []
            for v in values:
                success, _ = q.push(v)
                if success:
                    pushed.append(v)
                else:
                    response["message"] = "도중 큐가 가득 차서 일부만 Push 되었습니다."
                    break
            response["pushed_data"] = pushed
        else:
            success, msg = q.push(data.get("value"))
            response["success"] = success
            response["message"] = msg
            
    # 2) Pop
    elif action == "pop":
        success, res = q.pop()
        response["success"] = success
        response["data"] = res
        
    # 3) 현재 데이터 개수
    elif action == "size":
        response["size"] = q.get_size()
        
    # 4) 상태 검사 (full, empty)
    elif action == "status":
        response["is_full"] = q.is_full()
        response["is_empty"] = q.is_empty()
        
    # 5) 전면(Front) 데이터 확인
    elif action == "front":
        success, res = q.get_front()
        response["success"] = success
        response["front_data"] = res
        
    # 6) 큐 전체 데이터 삭제
    elif action == "clear":
        q.clear()
        response["message"] = "큐의 모든 데이터가 삭제되었습니다."
        
    # 7) 값의 index 검색
    elif action == "index":
        success, idx = q.index_of(data.get("value"))
        response["exists"] = success
        response["index"] = idx
        
    # 8) 값의 개수
    elif action == "count":
        response["count"] = q.count_of(data.get("value"))
        
    # 9) 값의 존재 여부 검사
    elif action == "exists":
        response["exists"] = q.exists(data.get("value"))
        
    # 10) Front부터 Rear까지 출력
    elif action == "print":
        response["elements"] = q.get_elements()
        
    else:
        return jsonify({"status": "error", "message": "알 수 없는 action 입니다."}), 400

    return jsonify(response), 200


if __name__ == "__main__":
    # Cloud Run 환경 변수 포트 바인딩 및 외부 접속 허용(0.0.0.0)
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

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

    def init(self, capacity):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front_idx = 0
        self.rear_idx = 0
        self.count = 0

    def is_empty(self):
        return self.count == 0

    def is_full(self):
        return self.count == self.capacity

    def push(self, data):
        if self.is_full():
            return False, "큐가 가득 찼습니다 (Full)"
        self.queue[self.rear_idx] = data
        self.rear_idx = (self.rear_idx + 1) % self.capacity
        self.count += 1
        return True, "Push 성공"

    def pop(self):
        if self.is_empty():
            return False, "큐가 비어 있습니다 (Empty)"
        data = self.queue[self.front_idx]
        self.queue[self.front_idx] = None
        self.front_idx = (self.front_idx + 1) % self.capacity
        self.count -= 1
        return True, data

    def get_size(self):
        return self.count

    def get_front(self):
        if self.is_empty():
            return False, "큐가 비어 있습니다"
        return True, self.queue[self.front_idx]

    def clear(self):
        self.init(self.capacity)

    def get_elements(self):
        elements = []
        for i in range(self.count):
            idx = (self.front_idx + i) % self.capacity
            elements.append(self.queue[idx])
        return elements

    def index_of(self, value):
        elements = self.get_elements()
        if value in elements:
            return True, elements.index(value)
        return False, -1

    def count_of(self, value):
        return self.get_elements().count(value)

    def exists(self, value):
        return value in self.get_elements()


q = FixedSizeQueue(20)


@app.route("/", methods=["GET"])
def health_check():
    return "Fixed-Size Queue Server is Running", 200


@app.route("/queue", methods=["POST"])
def manage_queue():
    data = request.get_json(silent=True) or {}
    action = data.get("action")
    
    # 🔍 Cloud Run 로그에 상세 분석 내용을 남기기 위한 print 출력 (flush=True 필수)
    print(f"================================================", flush=True)
    print(f"📥 [요청 분석] Action: '{action}' | 받은 Payload: {data}", flush=True)
    print(f"⚙️ [수행 전 상태] 데이터 개수: {q.get_size()}/{q.capacity} | 현재 요소: {q.get_elements()}", flush=True)

    response = {"status": "success", "action": action}

    if action == "init":
        cap = data.get("capacity", 20)
        q.init(cap)
        response["message"] = f"크기 {cap}인 큐로 초기화 되었습니다."
        
    elif action == "push":
        values = data.get("values", [])
        if isinstance(values, list):
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
            
    elif action == "pop":
        success, res = q.pop()
        response["success"] = success
        response["data"] = res
        
    elif action == "size":
        response["size"] = q.get_size()
        
    elif action == "status":
        response["is_full"] = q.is_full()
        response["is_empty"] = q.is_empty()
        
    elif action == "front":
        success, res = q.get_front()
        response["success"] = success
        response["front_data"] = res
        
    elif action == "clear":
        q.clear()
        response["message"] = "큐의 모든 데이터가 삭제되었습니다."
        
    elif action == "index":
        success, idx = q.index_of(data.get("value"))
        response["exists"] = success
        response["index"] = idx
        
    elif action == "count":
        response["count"] = q.count_of(data.get("value"))
        
    elif action == "exists":
        response["exists"] = q.exists(data.get("value"))
        
    elif action == "print":
        response["elements"] = q.get_elements()
        
    else:
        print(f"❌ [에러] 알 수 없는 Action 요구: {action}", flush=True)
        return jsonify({"status": "error", "message": "알 수 없는 action 입니다."}), 400

    print(f"📤 [수행 후 상태] 큐 내 데이터: {q.get_elements()} | 반환 JSON: {response}", flush=True)
    print(f"================================================", flush=True)

    return jsonify(response), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

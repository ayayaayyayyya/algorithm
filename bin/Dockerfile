FROM python:3.9-slim

WORKDIR /app

# 환경변수 설정
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

EXPOSE 8080

# 앱 실행
CMD ["python", "main.py"]

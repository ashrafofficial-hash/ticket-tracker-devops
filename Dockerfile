FROM python:3.11-slim
LABEL org.opencontainers.image.source="https://github.com/ashrafofficial-hash/ticket-tracker-devops"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

RUN mkdir -p /app/instance

EXPOSE 5000

CMD ["python", "-m", "app.main"]

FROM python:3.11-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels

FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 APP_PORT=8080
WORKDIR /app
RUN adduser --disabled-password --gecos '' appuser
COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/* && rm -rf /wheels
COPY . /app
EXPOSE 8080
USER appuser
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8080"]

FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["pytest", "--cov=engagement_engine", "--cov-report=term"]

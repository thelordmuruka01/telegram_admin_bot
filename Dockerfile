FROM python:3.12-slim

# Avoid .pyc files and enable unbuffered stdout for cleaner logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# BOT_TOKEN and other config should be passed at runtime via
# `docker run -e BOT_TOKEN=...` or a mounted .env file / compose env.
CMD ["python", "main.py"]

FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    zip \
    curl \
    rclone \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /scripts

COPY backup.py .
COPY restore.py .

CMD ["python", "backup.py"]

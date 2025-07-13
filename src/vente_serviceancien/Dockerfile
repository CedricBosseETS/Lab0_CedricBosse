FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app

# 1. Installer les dépendances système nécessaires pour mysqlclient
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    build-essential \
    mariadb-client \
    pkg-config \
    libmariadb-dev \
    bash \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 2. Copier et installer les dépendances Python
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

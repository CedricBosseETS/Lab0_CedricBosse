# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Définir le dossier de travail principal
WORKDIR /app

# Définir le PYTHONPATH pour inclure le dossier src
ENV PYTHONPATH=/app/src

# Installer bash, MySQL client utils (mysqladmin), et outils de compilation
RUN apt-get update && apt-get install -y \
    bash \
    default-libmysqlclient-dev \
    mariadb-client \
    gcc \
    build-essential \
    pkg-config \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copier les requirements et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier les sources, les tests et le script wait-for-it
COPY src/ src/

# Copier le script start.sh
COPY start.sh start.sh
RUN chmod +x start.sh

CMD ["bash", "start.sh"]

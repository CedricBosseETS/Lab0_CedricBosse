# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Définir le dossier de travail principal
WORKDIR /app

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
COPY . .

RUN chmod +x start.sh

CMD ["bash", "start.sh"]

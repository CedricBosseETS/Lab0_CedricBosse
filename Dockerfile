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
COPY test_files/ test_files/
COPY wait-for-it.sh wait-for-it.sh
RUN chmod +x wait-for-it.sh

# Copier le fichier pytest.ini si tu en as un
COPY pytest.ini .

# Copier le script start.sh
COPY start.sh start.sh
RUN chmod +x start.sh

# Démarrage : attend la DB puis exécute start.sh
CMD ["bash", "wait-for-it.sh", "db:3306", "--", "bash", "start.sh"]

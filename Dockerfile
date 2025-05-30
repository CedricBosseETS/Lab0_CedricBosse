# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Définir le dossier de travail principal
WORKDIR /app

# Définir le PYTHONPATH pour inclure le dossier src
ENV PYTHONPATH=/app/src

# Installer bash, MySQL client libs, et outils de compilation
RUN apt-get update && apt-get install -y \
    bash \
    default-libmysqlclient-dev \
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

# Définir la commande par défaut (sera remplacée plus tard par gestion via Django)
CMD ["bash", "wait-for-it.sh", "db:3306", "--", "python", "src/app.py"]

# syntax=docker/dockerfile:1
FROM python:3.11-slim

WORKDIR /app/src

ENV PYTHONPATH=/app/src

RUN apt-get update && apt-get install -y bash

RUN pip install cryptography

# Copier requirements.txt à la racine /app (hors src)
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

# Copier le dossier src dans /app/src
COPY src/ /app/src/

# Copier le script wait-for-it.sh dans /app/
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Commande par défaut : utiliser wait-for-it depuis /app, puis lancer python app.py dans /app/src
CMD ["bash", "/app/wait-for-it.sh", "db:3306", "--", "python", "app.py"]

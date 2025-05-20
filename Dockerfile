FROM python:3.10-slim

ENV PYTHONPATH=/app

WORKDIR /app

COPY . .

EXPOSE 5000

CMD ["python", "src/app.py"]

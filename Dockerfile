FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN apt-get update && apt-get install -y postgresql-client libmagic1 && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
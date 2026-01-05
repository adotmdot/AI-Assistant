# ---- Base image ----
FROM python:3.12-slim

# ---- Set working directory ----
WORKDIR /app

# ---- Install system deps ----
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ---- Copy requirements first (layer caching) ----
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy app code ----
COPY app ./app


# ---- Expose port ----
EXPOSE 8000

# ---- Run app ----
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

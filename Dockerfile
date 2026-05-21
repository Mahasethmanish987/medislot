# ---------- Stage 1: Builder ----------
FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /venv

WORKDIR /app
COPY requirements.txt .

RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

# ---------- Stage 2: Runtime ----------
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /venv /venv
COPY --from=builder /app /app

WORKDIR /app

ENV PATH="/venv/bin:$PATH"

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
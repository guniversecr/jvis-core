FROM python:3.12-slim AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS development
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt
COPY . .
CMD ["flask", "--app", "src.app:create_app", "run", "--reload", "--host", "0.0.0.0", "--port", "8000"]

FROM base AS production
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--factory", "src.app:create_app"]

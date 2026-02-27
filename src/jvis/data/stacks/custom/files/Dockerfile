FROM python:3.12-slim AS base
WORKDIR /app
COPY . .

FROM base AS development
CMD ["python", "-m", "src.main"]

FROM base AS production
CMD ["python", "-m", "src.main"]

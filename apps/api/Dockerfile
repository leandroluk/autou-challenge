FROM python:3.13-slim AS builder

WORKDIR /app

RUN pip install uv --no-cache-dir

COPY pyproject.toml .
COPY src ./src

RUN uv build --wheel --out-dir /dist


FROM python:3.13-slim

WORKDIR /app

COPY --from=builder /dist/*.whl /dist/

RUN pip install --no-cache-dir /dist/*.whl && rm -rf /dist

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
ENV HTTP_HOST=0.0.0.0 \
    HTTP_PORT=8000 \
    HTTP_BASE_PATH=/api/v1 \
    HTTP_DOCS_PATH=/docs \
    HTTP_REDOC_PATH=/redoc \
    HTTP_ENABLE_RELOAD=false \
    HTTP_TITLE="AutoU Email Analisys API" \
    HTTP_VERSION=1.0.0 \
    HTTP_DESCRIPTION="Email Analisys API - AutoU challenge." \
    PROVIDER_EMAIL_ANALYZER=httpx \
    PROVIDER_FILE_CONVERTER=fitz

EXPOSE 8000

CMD ["python", "-m", "src"]
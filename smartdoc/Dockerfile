FROM python:3.12-slim AS builder

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY poetry.lock pyproject.toml /app/

RUN poetry install --only main --no-root

FROM python:3.12-slim AS final

WORKDIR /app

COPY --from=builder /app /app

COPY . /app

EXPOSE 8000
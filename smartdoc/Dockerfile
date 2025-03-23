FROM python:3.12.8-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false

RUN poetry install --only main --no-root

COPY init.sh /app/init.sh

COPY . /app

EXPOSE 8000

ENTRYPOINT ["/app/init.sh"]
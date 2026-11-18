FROM docker.io/library/python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:0.13.9 /uv /usr/local/bin/uv

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends openssh-client \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project --no-cache --python /usr/local/bin/python

COPY main.py /app/main.py

EXPOSE 8000

ENTRYPOINT ["/app/.venv/bin/python", "main.py"]

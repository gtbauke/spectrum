FROM python:3.13-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.8.0 /uv /uvx /bin/

ADD . /app
WORKDIR /app

RUN uv sync --locked

COPY .env ./

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

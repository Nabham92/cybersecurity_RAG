FROM python:3.12-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.9.8 /uv /uvx /bin/

WORKDIR /app

COPY requirements.txt requirements.txt

RUN uv pip install --system -r requirements.txt

COPY . . 

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
FROM python:3.11-slim
LABEL maintainer="adamj"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock /app/

COPY ./ /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-root

ENV PYTHONPATH=/app

WORKDIR /app

CMD ["python3", "./payrolls/main.py"]

FROM python:3.10-slim

RUN apt-get update && apt-get install -y build-essential libmariadb-dev gcc

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --only main --no-root

COPY msp .

EXPOSE 8000

CMD ["gunicorn", "marking_system.wsgi:application", "--bind", "0.0.0.0:8000"]

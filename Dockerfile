FROM python:3.12-slim AS builder

# Устанавливаем зависимости для сборки
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
ENV POETRY_VERSION=1.9.0
RUN pip install poetry

# Создаём рабочую директорию
WORKDIR /app

# Копируем только файлы с зависимостями для кэширования
COPY pyproject.toml poetry.lock* /app/

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-root --no-ansi --only main

# ---- Stage 2: Runtime ----
FROM python:3.12-slim AS runtime

# Копируем зависимости из билд-стейджа
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
WORKDIR /app
# Копируем код приложения
COPY . .
ENV PYTHONPATH=/app/app
ENV PYTHONUNBUFFERED=1
# Прокси за nginx или docker-compose будет слушать 8000
EXPOSE 8000

# Переменные окружения (можно перенести в .env)
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

# Команда запуска
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
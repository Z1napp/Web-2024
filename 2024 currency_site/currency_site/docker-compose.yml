# Використовуємо базовий образ Python
FROM python:3.9-slim

# Встановлюємо робочу директорію в контейнері
WORKDIR /app

# Копіюємо файли проекту до контейнера
COPY . /app

# Встановлюємо залежності
RUN pip install --no-cache-dir fastapi uvicorn jinja2 requests

# Вказуємо порт, який буде використовувати додаток
EXPOSE 8000

# Команда для запуску серверу
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.10-slim

# Робоча директорія
WORKDIR /app

# Копіюємо залежності
COPY requirements.txt .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо решту коду
COPY . .

# Відкриваємо порт
EXPOSE 8000

# Запуск
CMD ["python", "app.py"]

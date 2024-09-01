# Используем базовый образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы req.txt и устанавливаем зависимости
COPY req.txt req.txt
RUN pip install --no-cache-dir -r req.txt

# Копируем все файлы проекта в рабочую директорию
COPY . .

# Устанавливаем переменные окружения для настройки
ENV PYTHONUNBUFFERED=1

# Запуск бота
CMD ["python", "telegram_bot.py"]

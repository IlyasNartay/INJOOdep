# Используем базовый образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

# Делаем start.sh исполняемым
RUN chmod +x start.sh start_bot.sh start_migrate.sh

# Указываем переменные окружения (если надо)
ENV PYTHONUNBUFFERED=1

# Запускаем стартовый скрипт
CMD ["./start.sh"]

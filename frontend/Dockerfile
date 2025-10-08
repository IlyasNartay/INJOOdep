# --- Этап сборки (Builder Stage) ---
# Используем официальный образ Node.js LTS для сборки
FROM node:20-alpine AS builder

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем только файлы package.json и package-lock.json для установки зависимостей
# Это позволяет Docker кэшировать этот слой, если зависимости не изменились
COPY package*.json ./

# Устанавливаем зависимости проекта
# Используем --omit=dev, чтобы не устанавливать devDependencies в production-сборке,
# так как они не нужны для рантайма приложения.
# Если у вас есть devDependencies, которые нужны для сборки (например, компиляторы),
# убедитесь, что они устанавливаются до этапа RUN npm run build
# В противном случае, если npm run build не нуждается в devDependencies,
# можно использовать только npm ci (npm clean install)
# RUN npm ci --omit=dev
RUN npm install

# Копируем остальные файлы проекта (включая .env.production)
# В этот момент .env.production должен быть в корне frontend папки
COPY . .
# Запускаем сборку фронтенд-приложения
# Vite автоматически подхватит .env.production, если он находится в корне
RUN npm run build

# --- Этап продакшн-сервера Nginx ---
# Используем легковесный официальный образ Nginx для продакшн
FROM nginx:alpine

# Копируем собранные статические файлы из этапа builder в директорию Nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Опционально: Если у вас есть кастомный Nginx-конфиг для фронтенда, скопируйте его
# Например, для редиректов SPA или кастомных заголовков
# COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Открываем порт 80, который Nginx слушает по умолчанию
EXPOSE 80

# Запускаем Nginx в фоновом режиме
CMD ["nginx", "-g", "daemon off;"]
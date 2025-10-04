# Этапы сборки могут варьироваться (например, если вы используете Node.js для сборки)

# Этап 1: Сборка фронтенда (если необходимо)
FROM node:lts-alpine as builder
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
# Пример команды сборки React/Vue/Vite:
RUN npm run build

# Этап 2: Запуск с Nginx
FROM nginx:alpine
# Скопировать вашу конфигурацию Nginx
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Скопировать собранные статические файлы из этапа builder (предполагаем, что они в папке /app/dist)
# !!! ПУТЬ /app/dist МОЖЕТ ОТЛИЧАТЬСЯ В ЗАВИСИМОСТИ ОТ ВАШЕГО СБОРЩИКА (build, public, dist) !!!
COPY --from=builder /app/dist /usr/share/nginx/html

# Порт 80 открыт внутри контейнера, Traefik будет направлять трафик сюда
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
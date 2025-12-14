# =========================
# 1. Frontend build stage
# =========================
FROM node:18 AS frontend-build
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend .
RUN npm run build


# =========================
# 2. Backend + Nginx runtime
# =========================
FROM python:3.10-slim

WORKDIR /app

# Install system deps + nginx
RUN apt-get update && apt-get install -y \
    nginx \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Backend dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Backend source
COPY backend ./backend

# Frontend build output
COPY --from=frontend-build /app/frontend/dist /usr/share/nginx/html

# Nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Railway provides PORT automatically
EXPOSE $PORT

# Start backend + nginx
CMD bash -c "\
uvicorn backend.main:app --host 127.0.0.1 --port 8000 & \
nginx -g 'daemon off;'"

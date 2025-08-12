FROM node:20-slim

WORKDIR /app
COPY frontend/package.json frontend/package-lock.json* /app/
RUN npm ci
COPY frontend /app

EXPOSE 3000
ENV HOST 0.0.0.0
CMD ["npm","run","dev"]

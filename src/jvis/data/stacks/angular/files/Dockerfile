FROM node:20-alpine AS base
WORKDIR /app
COPY package.json package-lock.json* yarn.lock* ./
RUN npm install

FROM base AS development
COPY . .
CMD ["npx", "ng", "serve", "--host", "0.0.0.0"]

FROM base AS build
COPY . .
RUN npx ng build --configuration production

FROM nginx:alpine AS production
COPY --from=build /app/dist/*/browser /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

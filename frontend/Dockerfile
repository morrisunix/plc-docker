# FROM node:20 AS build

# WORKDIR /app
# COPY package*.json ./
# RUN npm install

# COPY . .
FROM morrisunix/plc-frontend:latest as build
WORKDIR /app

# Set the environment variable for the build stage
ARG REACT_APP_BACKEND_IP
ARG REACT_APP_BACKEND_PORT
ENV REACT_APP_BACKEND_IP=$REACT_APP_BACKEND_IP
ENV REACT_APP_BACKEND_PORT=$REACT_APP_BACKEND_PORT

RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80

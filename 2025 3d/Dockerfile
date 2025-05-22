FROM node:18-alpine

RUN npm install -g http-server

WORKDIR /usr/src/app
COPY . .

EXPOSE 8000

CMD ["http-server", "-p", "8000", "-a", "0.0.0.0"]

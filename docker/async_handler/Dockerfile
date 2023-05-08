FROM node:18.12-alpine3.16

WORKDIR /app
COPY async_handler/package.json async_handler/yarn.lock .
RUN yarn install

COPY async_handler .
RUN yarn build

ENTRYPOINT yarn start
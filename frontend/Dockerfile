FROM node:19-alpine3.15

WORKDIR /frontend
COPY package.json .
COPY package-lock.json .
RUN npm install

RUN mkdir node_modules/.cache && chmod -R 777 node_modules/.cache

COPY . .

CMD ["npm", "run", "start"]

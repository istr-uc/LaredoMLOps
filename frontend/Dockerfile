# frontend/Dockerfile
FROM node:22-alpine AS prod

WORKDIR /app

# COPY laredo-app/package.json /app

RUN npm install -g npm@11.4.1

COPY laredo-app/ /app/

RUN npm install --legacy-peer-deps

RUN npm run build

FROM nginx:alpine

WORKDIR /usr/local/bin

COPY --from=prod /app/dist /usr/share/nginx/html

COPY generate-config.sh .

COPY custom-nginx.template /etc/nginx/conf.d/

RUN chmod +x generate-config.sh

EXPOSE 80

ENTRYPOINT [ "/bin/sh", "generate-config.sh"]

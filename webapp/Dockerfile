FROM node:12-alpine AS builder
WORKDIR /webapp
COPY . /webapp/
RUN npm install --silent
RUN npm install react-scripts@3.0.1 -g --silent
RUN npm run build

FROM nginx:1.14.2
WORKDIR /webapp
COPY --from=builder /webapp/build /usr/share/nginx/html
EXPOSE 3000 80
CMD ["nginx", "-g", "daemon off;"]

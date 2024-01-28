FROM nginx:1.19.0-alpine

# Install openssl
RUN apk --no-cache add openssl

# Create SSL directory
RUN mkdir -p /etc/nginx/ssl

# Generate self-signed SSL certificate
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt \
    -subj "/CN=localhost"

COPY ./default.conf /etc/nginx/conf.d/default.conf 



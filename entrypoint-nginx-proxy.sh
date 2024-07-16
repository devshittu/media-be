#!/bin/sh

# Create required directories
mkdir -p /etc/nginx/conf.d
mkdir -p /usr/share/nginx/html/.well-known/acme-challenge
mkdir -p /etc/nginx/vhost.d
mkdir -p /etc/nginx/certs

# Execute the original command
exec "$@"

# entrypoint-nginx-proxy.sh
#!/bin/sh

# Create required directories
mkdir -p /etc/nginx/conf.d
mkdir -p /usr/share/nginx/html/.well-known/acme-challenge

# Execute the original command
exec "$@"

# entrypoint-nginx-proxy.sh
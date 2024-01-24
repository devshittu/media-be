#!/bin/sh

while ! nc -z web-app 8000; do
  echo "Waiting for the web-app service to start..."
  sleep 1
done

# Start Nginx after the loop exits
nginx -g "daemon off;"

# nginx-conf/start-nginx.sh

# /Users/mshittu/programming-projects/python/django/media-be/nginx-conf/start-nginx.sh
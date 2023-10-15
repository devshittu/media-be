#!/bin/bash

while ! nc -z web 8000; do
  echo "Waiting for the web service to start..."
  sleep 1
done

# Start Nginx after the loop exits
nginx -g "daemon off;"

# nginx-conf/start-nginx.sh
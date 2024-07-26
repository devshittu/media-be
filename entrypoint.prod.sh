#!/bin/sh

# if [ "$POSTGRES_DB" = "mediabedb" ]
# then
#     echo "Waiting for postgres..."

#     while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
#       sleep 0.1
#     done

#     echo "PostgreSQL started"
# fi

# Function to wait for a service to be ready
wait_for_service() {
  local service=$1
  local port=$2
  echo "Waiting for $service to be ready on port $port..."
  while ! nc -z $service $port; do
    sleep 0.1
  done
  echo "$service is ready!"
}

# Wait for PostgreSQL to be ready
if [ "$POSTGRES_DB" = "mediabedb" ]; then
  wait_for_service $POSTGRES_HOST $POSTGRES_PORT
fi

# Wait for Neo4j to be ready
if [ "$NEO4J_HOST" = "db-neo4j" ]; then
  wait_for_service $NEO4J_HOST $NEO4J_PORT
fi

exec "$@"

# entrypoint.prod.sh

#!/bin/sh

# Function to wait for a service to be ready
wait_for_service() {
  local service=$1
  local port=$2
  echo "Waiting for $service to be ready on port $port..."
  while ! nc -z $service $port; do
    echo "Waiting for $service to be ready..."
    sleep 5
  done
  echo "$service is ready!"
}

# Wait for Neo4j to be ready
wait_for_service $NEO4J_HOST $NEO4J_PORT

# Wait for Elastic to be ready
wait_for_service $ELASTICSEARCH_HOST $ELASTICSEARCH_PORT

# Run Django setup commands
echo "Running Django setup commands..."
python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate
echo "--== Completed migration successfully ==--"
echo "..."
echo "> Installing the Neo4j labels"
python manage.py install_labels
echo "--== Completed label installation (Neo4j) successfully ==--"
echo "..."
echo "> Installing the seeds for both postgresdb "
python manage.py autoseed
echo "..."
echo "--== Completed autoseed successfully ==--"

echo "> Installing the seeds for neo4jdb"
python manage.py importstories
echo "..."
echo "--== Completed autoseed successfully ==--"

echo "> Installing/Building the indecies for elasticsearch"
python manage.py search_index --rebuild
echo "..."
echo "--== Completed building index successfully ==--"

# Create superuser - Use environment variables for email and password
echo "Creating superuser..."
echo "from django.contrib.auth import get_user_model; CustomUser = get_user_model(); CustomUser.objects.create_superuser(email='${DJANGO_SUPERUSER_EMAIL}', password='${DJANGO_SUPERUSER_PASSWORD}', username='${DJANGO_SUPERUSER_USERNAME}', display_name='${DJANGO_SUPERUSER_DISPLAY_NAME}', avatar_url='${DJANGO_SUPERUSER_AVATAR_URL}', has_completed_setup=${DJANGO_SUPERUSER_HAS_COMPLETED_SETUP})" | python manage.py shell

echo "Setup completed successfully!"

# k8s/scripts/init-web-app.sh

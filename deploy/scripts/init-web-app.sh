#!/bin/sh

# Wait for PostgreSQL to be ready
# echo "Waiting for PostgreSQL database..."
# while ! nc -z db-postgres 5432; do
#     sleep 1
# done
# echo "PostgreSQL database is ready!"

# # Wait for Neo4j to be ready
# echo "Waiting for Neo4j database..."
# while ! nc -z db-neo4j 7687; do
#     sleep 1
# done
# echo "Neo4j database is ready!"

# Run Django setup commands
echo "Running Django setup commands..."
python manage.py migrate
echo "--== Completed migration successfully ==--"
echo "..."
echo "> Installing the Neo4j labels"
python manage.py install_labels
echo "--== Completed label installation (Neo4j) successfully ==--"
echo "..."
echo "> Installing the seeds for both postgresdb and neo4jdb"
python manage.py autoseed
echo "..."
echo "--== Completed autoseed successfully ==--"

# Create superuser - Use environment variables for username and password
echo "Creating superuser..."
echo "from django.contrib.auth import get_user_model; CustomUser = get_user_model(); CustomUser.objects.create_superuser('${DJANGO_SUPERUSER_EMAIL}', '${DJANGO_SUPERUSER_PASSWORD}')" | python manage.py shell

echo "Setup completed successfully!"

# deploy/scripts/init-web-app.sh
#!/bin/sh
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
echo "> Installing the seeds for both postgresdb and neo4jdb"
python manage.py autoseed
echo "..."
echo "--== Completed autoseed successfully ==--"

# Create superuser - Use environment variables for email and password
echo "Creating superuser..."
echo "from django.contrib.auth import get_user_model; CustomUser = get_user_model(); CustomUser.objects.create_superuser(email='${DJANGO_SUPERUSER_EMAIL}', password='${DJANGO_SUPERUSER_PASSWORD}', username='${DJANGO_SUPERUSER_USERNAME}', display_name='${DJANGO_SUPERUSER_DISPLAY_NAME}', avatar_url='${DJANGO_SUPERUSER_AVATAR_URL}', has_completed_setup=${DJANGO_SUPERUSER_HAS_COMPLETED_SETUP})" | python manage.py shell

echo "Setup completed successfully!"

# k8s/scripts/init-web-app.sh

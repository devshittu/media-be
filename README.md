## Default docker commands
```shell
docker compose -f docker-compose.dev.yml up 

docker compose -f docker-compose.dev.yml build

docker compose -f docker-compose.dev.yml up --build
```

Open [http://localhost:8000](http://localhost:8000).

## Useful commands


```bash

# Stop all running containers
docker kill $(docker ps -aq) && docker rm $(docker ps -aq)

# Free space
docker system prune -af --volumes
```
## Resetting commands

```shell
docker kill $(docker ps -aq) && docker rm $(docker ps -aq)

docker system prune -af --volumes 

docker network create my_media_network

docker compose -f docker-compose.dev.yml up --build


```

## Available commands
### Non-docker.
```shell
python manage.py showmigrations
python manage.py makemigrations
python manage.py migrate
python manage.py show_urls --format=json #> app-urls.json
python manage.py autoseed

python manage.py install_labels
python manage.py importstories #load existing stories ids to create story nodes in the neo4j database
python manage.py deleteallneo # deletes any existing stories ids used to create story nodes in the neo4j database
python manage.py createsuperuser
# Email: test@test.co
# Password: test@test.co
# Bypass password validation and create user anyway? [y/N] y

python manage.py export_uri_constants --lang=[ts,java,php] 
```
### Docker
combine any of the available commands with the following
```shell
docker compose -f docker-compose.dev.yml exec web python manage.py *  #append any of the available commands

```
Go to [http://localhost:7474/browser/manage](http://localhost:7474/browser/)

Go to [http://localhost:8000/admin/](http://localhost:8000/admin)

## Installing
To install and perform migration the database, it includes creating all migrations, migrating them, and add test data in the Docker, you can follow these steps:
```shell
docker compose -f docker-compose.dev.yml exec web python manage.py  #append any of the available commands

```
## Resetting
To reset the database, remove all migrations, and data in Docker, you can follow these steps:

1. **Stop the Containers**:
   ```bash
   docker compose -f docker-compose.dev.yml down -v
   ```

2. **Remove the Database Volume**:
   This will delete all the data in your PostgreSQL database.
   ```bash
   docker volume rm media-be_postgres_data media-be_neo4j_data media-be_neo4j_logs
   ```

3. **Remove Migrations**:
   You'll need to delete all the migration files except for the `__init__.py` file in each app's `migrations` directory. You can do this manually or use a command like:
   ```bash
   find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
   find . -path "*/migrations/*.pyc" -delete
   ```

4. **Rebuild the Containers**:
   Since you've made changes, it's a good idea to rebuild the containers.
   ```bash
   docker compose -f docker-compose.dev.yml build
   ```

5. **Start the Containers**:
   ```bash
   docker compose -f docker-compose.dev.yml up -d
   ```

6. **Run Migrations**:
   Now, you'll need to recreate the database schema by running migrations.
   ```bash
   docker compose -f docker-compose.dev.yml exec web python manage.py makemigrations
   docker compose -f docker-compose.dev.yml exec web python manage.py migrate
   ```

After these steps, your database should be reset, and all the previous data and migrations will be removed. You'll have a fresh database to work with.
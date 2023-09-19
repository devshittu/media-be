```shell

python manage.py showmigrations
python manage.py migrate
python manage.py makemigrations
```
```shell
docker compose -f docker-compose.dev.yml up 

docker compose -f docker-compose.dev.yml build

docker compose -f docker-compose.dev.yml up --build
```
```shell
docker compose -f docker-compose.dev.yml exec web python manage.py makemigrations

docker compose -f docker-compose.dev.yml exec web python manage.py migrate


```

Open [http://localhost:8000](http://localhost:8000).

## Useful commands


```bash
# Create a network, which allows containers to communicate
# with each other, by using their container name as a hostname
docker network create my_network

# Stop all running containers
docker kill $(docker ps -aq) && docker rm $(docker ps -aq)

# Free space
docker system prune -af --volumes
```
## Resetting commands

```shell
docker kill $(docker ps -aq) && docker rm $(docker ps -aq)

docker system prune -af --volumes 

docker network create my_network

docker compose -f docker-compose.dev.yml up --build


```

## Django commands

```shell
python manage.py showmigrations
python manage.py makemigrations
python manage.py migrate
python manage.py autoseed
python manage.py createsuperuser
# Email: test@test.co
# Password: test@test.co
# Bypass password validation and create user anyway? [y/N] y

```


## Installing

```shell
docker compose -f docker-compose.dev.yml exec web python manage.py 

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
   docker volume rm your_project_name_postgres_data
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
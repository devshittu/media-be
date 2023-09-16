```shell
python manage.py makemigrations
python manage.py migrate
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
python manage.py migrate
python manage.py makemigrations

```


## Installing

```shell
docker compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
# Email: test@test.co
# Password: test@test.co
# Bypass password validation and create user anyway? [y/N]: y: 
```
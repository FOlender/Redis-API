# Redis-API

[Redis](https://redis.io/) API written in Python to solve "Basic Implementation" of the [ML Challenge](https://github.com/irt-mercadolibre/challenge_redis_FOlender).

## Installation

1.  Install [Git](https://git-scm.com/downloads)
2.  Install [Docker](https://www.docker.io/).
3.  Pull from Github Repo:
```
mkdir Redis-API && cd Redis-API/ && git init && git pull https://github.com/FOlender/Redis-API.git
```
4.  Run Dockerfile:
```
sudo docker build . -t redis-api:v1
```
5. Execute container:
``` 
sudo docker run --rm -d --name Redis-APIv1 -p 8080:8080 redis-api:v1 bash -c "redis-server & python3 /Redis-API/Redis-API.py"
```

## Usage

#### PUSH:
```
curl -X POST -i http://localhost:8080/api/queue/push --data 'Escriba su mensaje aqui por favor.'
```
- Add new message to the queue.

#### POP:
```
curl -X POST -i http://localhost:8080/api/queue/pop
```
- Return the whole queue of messages.

### Count:
```
curl -X GET -i http://localhost:8080/api/queue/count
```
- Return the number of messages in the queue.

### Delete All:
```
curl -X POST -i http://localhost:8080/api/queue/deleteall
```
- Removes every message from the queue.

## Maintenance

If the container was runned with the "-rm" argument as indicated in step 5 of the installation process, the container will be remove when stoped, so it is highly recommended to generate new images from the running container once in a while to backup the new rules added to it:
```
# sudo docker commit Redis-API redis-api:v2
```

## DIY

#### Get the code from GitHub and Modify it...

1.  Create local directory and initiate git
```
mkdir Redis-API && cd Redis-API/ && git init
```
2.  Pull Repo from Github:
```
git pull https://github.com/FOlender/Redis-API.git
```
3. Do whatever you want with the code.
4.  Commit changes and Push to Github:
```
git add .
git commit -m 'Message'
git remote add origin https://github.com/FOlender/Redis-API.git
git branch -m master main
git push -u origin main
```

#### Get into the running container to see under the hood...

```
sudo docker exec -i -t Redis-APIv1 /bin/bash
```

## TODO

- [] Replace base image ubuntu:stable with alpine:stable or redis:stable
- [x] Add RemoveAll endpoint.

## Issues

Bugs? Missing features? Errors in the documentation? [Let me know](https://github.com/FOlender/Redis-API/issues/new).

## Notas para ML:

- N/A


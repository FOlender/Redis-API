# Redis-API

[Redis](https://redis.io/) API written in Python to solve "Basic Implementation" of the [ML Challenge](https://github.com/irt-mercadolibre/challenge_redis_FOlender).

## Installation

1.  Install [Git](https://git-scm.com/downloads)
2.  Install [Docker](https://www.docker.io/).
3.  Pull from Github Repo:
```
mkdir Redis-API && cd Redis-API/ && git init && git pull https://github.com/FOlender/Redis-API.git v2
```
4.  Run Dockerfile:
```
sudo docker build . -t redis-api:v2
```
5. Execute container:
``` 
sudo docker run --rm -d --name Redis-APIv2 -p 8080:8080 redis-api:v2 bash -c "redis-server & python3 /Redis-API/Redis-API.py"
```

## Usage

#### PUSH:

```
curl -X POST -i http://localhost:8080/api/queue/push --data 'Escriba su mensaje aqui por favor.' -H 'Token: XXXXXXXXXXXXXXXXXXXXXXXXX'
```
- Add new message to the queue.

#### POP:

```
curl -X POST -i http://localhost:8080/api/queue/pop
```
- Return the last message of the queue (see POP ALL for the whole queue).

### Count:

```
curl -X GET -i http://localhost:8080/api/queue/count
```
- Return the number of messages in the queue.

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
sudo docker exec -i  Redis-APIv2 /bin/bash
```

#### What is Redis doing?

```
sudo docker exec -i -t Redis-APIv2 redis-cli monitor
```

## TODO

- [] Replace base image ubuntu:stable with alpine:stable or redis:stable
- [] Funcionalidades pendientes: DeleteLast
- [] Pop (ALL y Batch): Ordenar resultados por orden de llegada.
- [] Redis: Hardenizar "/etc/redis/redis.conf"

## Issues

Bugs? Missing features? Errors in the documentation? [Let me know](https://github.com/FOlender/Redis-API/issues/new).

## Notas para ML (& Bonus):

### Autenticación

Autenticacion a partir de Token generado dinamicamente cuando se crea la imagen con Dockerfile:
```
...
Token de Autentication: XXXXXXXXXXXXXXXXXXXXXXXXX
...
```

Adicionalmente pueden visualizar el token en el archivo "/Redis-API/Token" dentro del contenedor en ejecucion:

```
sudo docker exec -i Redis-APIv2 cat /Redis-API/Token
```

La autenticacion solamente es forzada cuando se realizan cambios (Agregar mensajes a la cola, eliminar todos los mensajes, etc.) o cuando se accede a endpoints confidenciales (Ej: metrics).

### Funcionalidades adicionales

#### Delete All

Elimina todos los mensajes de la cola:
```
curl -X POST -i http://localhost:8080/api/queue/deleteall -H 'Token: XXXXXXXXXXXXXXXXXXXXXXXXX'
```

#### Pop all

Ver todos los mensajes de la cola. Mismo Endpoint que el POP original pero el Body debera contener la palabra ALL:
```
curl -X POST -i http://localhost:8080/api/queue/pop -d 'ALL'
```
- Esta funcionalidad se genero a partir de que en el enunciado no quedaba claro si el POP original era para el ultimo mensaje o para todos los mensajes. 

### Logs

- Path: /Redis-API/Redis-API.log
- Default Log Level: INFO en Python + DEBUG en Flask
- Modificacion de Log Level: Ver variables "LogLevel" y "FlaskDebug" al inicio del script.

### Pop y Push en batch

#### PUSH (BATCH)

Mismo Endpoint que el PUSH original pero enviando con formato y content-type JSON. Ejemplo: 
```
curl -X POST -H 'content-type: application/json' -i http://localhost:8080/api/queue/push -H 'Token: XXXXXXXXXXXXXXXXXXXXXXXXX' --data '{
	"msg1": "Primer mensaje",
	"msg2": "Segundo mensaje",
	"Mensaje3": "Tercer \n y no ultimo \r\n mensaje",
	"mnsg4":"Cuarto (y ultimo) mensaje",
	"5": "Mensaje nro.: 5"
}' 
```

#### POP (BATCH)

Mismo Endpoint que el POP original pero el Body debera contener el listado de Keys separados por coma correspondiente a los mensajes deseados: 
```
curl -X POST -i http://localhost:8080/api/queue/pop --data '1,2,5,6'
```

### Métricas
```
curl -X POST -i http://localhost:8080/api/metrics
```
- Devolvera cantidad de requests exitosos a cada Endpoint.

### Endpoint de estado de salud de Redis.

```
curl -X POST -i http://localhost:8080/api/redis/health -H 'Token: XXXXXXXXXXXXXXXXXXXXXXXXX'
```
- Devolvera informacion y estado de salud de Redis.


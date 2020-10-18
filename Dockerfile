# Descarga de imagen base de Docker "Ubuntu".
FROM ubuntu:latest

# Actualizo e instalo requerimientos.
RUN apt-get update -y && apt-get upgrade -y && apt-get install python3 python3-pip redis-server -y
RUN pip3 install flask flask-restful redis flask_redis

# Copio API.
RUN mkdir /Redis-API/
COPY --chown=root:root Redis-API.py /Redis-API/Redis-API.py
RUN chmod 755 /Redis-API/Redis-API.py

# Preparo la ejecucion
WORKDIR /Redis-API/
EXPOSE 8080
CMD [ "python3", "./Redis-API.py" ]

# Genero Token Random y notifico
RUN head /dev/urandom | tr -dc A-Za-z0-9 | head -c 25 > /Redis-API/Token 
RUN echo "Token de Autentication: " `cat /Redis-API/Token`


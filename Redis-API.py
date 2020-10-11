#import redis
from flask_redis import FlaskRedis
from flask import Flask, request

app = Flask(__name__)

# Push
@app.route('/api/queue/push', methods=['POST'])
def queuepush():
	# Capturo Mensaje
	Mensaje = request.data
	# Determino longitud de cola de mensajes de Redis
	RedisLength = len(redis_client.keys('*'))
	# Agrego el nuevo mensaje a la cola
	redis_client.set(RedisLength,Mensaje)
	# Envio respuesta
	Response = {'status':'ok'}
	return Response

# Pop
@app.route('/api/queue/pop', methods=['POST'])
def queuepop():
	Response = {}
	for x in redis_client.keys('*'):
		Response[x] = redis_client.get(x)
	Response['status'] = 'ok'
	return Response

# Count
@app.route('/api/queue/count', methods=['GET'])
def queuecount():
	# Calculo cantidad de mensajes
	RedisLength = len(redis_client.keys('*'))
	# Envio respuesta en forma de diccionario.
	Response = {'status':'ok', 'count':RedisLength}
	return Response

if __name__ == '__main__':
	redis_client = FlaskRedis(app)
	app.run(host = '0.0.0.0', port=int("8080"), debug=True) 
	# Debug se mantiene en True para que el error sea detallado al consumir la API.


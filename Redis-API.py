# Importar modulos
import os
import sys
from flask_redis import FlaskRedis
from flask import Flask, request, jsonify
from multiprocessing import Value
import subprocess
import logging

# Inicializar variables
app = Flask(__name__)
ScriptName = os.path.basename(__file__)
LogLevel=logging.DEBUG # Opciones: .CRITICAL, .ERROR, .WARNING, .INFO, .DEBUG
FlaskDebug=True # Opciones: True, False

# Inicializo metricas
Pushs = Value('i', 0)
Pops = Value('i', 0)
DeletesAll = Value('i', 0)
Counts = Value('i', 0)
RedisHealths = Value('i', 0)

# Logs
logging.basicConfig(filename='Redis-API.log',level=LogLevel,format='%(asctime)s %(levelname)s: %(message)s')
logging.info('------------------------- ' + ScriptName +  ' -------------------------')

# Detectar Token generado con Imagen de Docker
if not os.path.exists("./Token"): 
	logging.critical('Token File not detected in Docker Image')
	sys.exit("Token File not detected in Docker Image")
TokenFile = open("./Token", "r")
HardToken = TokenFile.read()
if not HardToken: 
	logging.critical('Token not found in file ./Token on the Docker Image')
	sys.exit("Token not found in file ./Token on the Docker Image")
TokenFile.close()
logging.info('Token: ' + HardToken)

# Iniciar redis-server
logging.info('*** Starting Redis-Server ***')
bashCommand = "redis-server --daemonize yes"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
logging.debug(output)
if error: logging.error(error)

# Push
@app.route('/api/queue/push', methods=['POST'])
def queuepush():
	logging.info('Endpoint: /api/queue/push')
	logging.debug('Method: ' + request.method)
	# Capturo y verifico Token
	Token = request.headers.get('Token')
	if not Token:
		logging.error('Token no detectado')
		return jsonify({"msg": "Missing Token Header"}), 400
	logging.debug('Token detectado: ' + Token)
	if Token != HardToken:
		logging.error('Token incorrecto: ' + Token) 
		return jsonify({"msg": "Bad Token"}), 401
	# Verifico si es un Batch de mensjaes (JSON) o un unico mensaje (NO JSON).
	if not request.is_json:
		# Capturo el Body como Mensaje Unico
		Mensaje = request.form
		for msg in Mensaje: Mensaje = msg
		RedisLength = len(redis_client.keys('*'))
		logging.debug('Key de Redis: ' + str(RedisLength))
		logging.debug('Mensaje: ' + Mensaje)
		redis_client.set(RedisLength,Mensaje)
	else:
		# Capturo Batch de mensajes en formato JSON
		Mensaje = request.get_json()
		for msg in Mensaje:
			RedisLength = len(redis_client.keys('*'))
			logging.debug('Key en Body: ' + msg)
			logging.debug('Key de Redis: ' + str(RedisLength))
			logging.debug('Mensaje: ' + Mensaje[msg])
			redis_client.set(RedisLength,Mensaje[msg])
	# Envio respuesta
	Response = {'status':'ok'}
	logging.info('Response Body: ' + str(Response))
	# Metricas
	Pushs.value += 1
	return Response

# Pop
@app.route('/api/queue/pop', methods=['POST'])
def queuepop():
	logging.info('Endpoint: /api/queue/pop')
	logging.debug('Method: ' + request.method)
	# Preparo el diccionario
	Response = {}
	
	# Capturo Body
	Mensaje = request.form
	# Si el Body esta vacio, devuelvo el ultimo mensaje de la queue.
	if not (Mensaje):
		RedisLength = len(redis_client.keys('*'))-1
		Value = redis_client.get(RedisLength)
		Mensaje = Value.decode()
		logging.debug('Key: ' + str(RedisLength) + ' | Mensaje: ' + Mensaje)
		Response[RedisLength] = Value
	else:
	# Si el Body contiene debera ser 'ALL' o un listado de valores numericos separados por coma (Batch).
		for msg in Mensaje: 
			if msg.upper() == 'ALL':
				for x in redis_client.keys('*'):
					Value = redis_client.get(x)
					Mensaje = Value.decode()
					Key = x.decode()
					logging.debug('Key: ' + str(Key) + ' | Mensaje: ' + Mensaje)
					Response[Key] = Mensaje
			else:
				logging.debug('Batch: ' + msg)
				msg = msg.split(',')
				RedisLength = len(redis_client.keys('*'))
				for x in msg:
					if x.isnumeric() and int(x) < int(RedisLength): 
						Value = redis_client.get(x)
						Mensaje = Value.decode()
						logging.debug('Key: ' + x + ' | Mensaje: ' + Mensaje) 
						Response[x] = Mensaje
	# Metricas
	Pops.value += 1
	# Termino de armar la respuesta.
	Response['status'] = 'ok'
	logging.debug('Response Body: ' + str(Response))
	return jsonify(Response), 200

# Count
@app.route('/api/queue/count', methods=['GET'])
def queuecount():
	logging.info('Endpoint: /api/queue/count')
	logging.debug('Method: ' + request.method)
	# Calculo cantidad de mensajes
	RedisLength = len(redis_client.keys('*'))
	logging.info('Count: ' + str(RedisLength))
	# Envio respuesta en forma de diccionario.
	Response = {'status':'ok', 'count':RedisLength}
	logging.debug('Response Body: ' + str(Response))
	# Metricas
	Counts.value += 1
	return Response

# DeleteAll
@app.route('/api/queue/deleteall', methods=['POST'])
def queuedeleteall():
	logging.info('Endpoint: /api/queue/deleteall')
	logging.debug('Method: ' + request.method)
	# Capturo y verifico Token
	Token = request.headers.get('Token')
	if not Token:
		logging.error('Token no detectado') 
		return jsonify({"msg": "Missing Token Header"}), 400
	if Token != HardToken:
		logging.error('Token incorrecto: ' + Token)  
		return jsonify({"msg": "Bad Token"}), 401
	# Calculo cantidad de mensajes
	RedisLength = len(redis_client.keys('*'))
	logging.debug('Cantidad de mensajes a eliminar: ' + str(RedisLength))
	# Elimino todas las entradas.
	for x in redis_client.keys('*'): 
		redis_client.delete(x)
		logging.debug(str(x) + ' Eliminado')
	# Envio respuesta en forma de diccionario.
	Response = {'status':'ok', 'count':RedisLength}
	logging.debug('Response Body: ' + str(Response))
	# Metricas
	DeletesAll.value += 1
	return Response

# Estado de salud de Redis
@app.route('/api/redis/health', methods=['POST'])
def redishealth():
	# Capturo y verifico Token
	Token = request.headers.get('Token')
	if not Token:
		logging.error('Token no detectado') 
		return jsonify({"msg": "Missing Token Header"}), 400
	if Token != HardToken:
		logging.error('Token incorrecto: ' + Token)  
		return jsonify({"msg": "Bad Token"}), 401
	logging.info('Endpoint: /api/redis/health')
	logging.debug('Method: ' + request.method)
	# Obtengo estado de salud de redis con redis-cli
	RedisHealth = subprocess.run(['redis-cli', 'INFO'], stdout=subprocess.PIPE)
	RedisHealth = RedisHealth.stdout.decode('utf-8')
	logging.debug('Redis Health: ')
	logging.debug(RedisHealth)
	# Metricas
	RedisHealths.value += 1
	return RedisHealth, 200

# Metricas
@app.route('/api/metrics', methods=['POST'])
def metrics():
	logging.info('Endpoint: /api/metrics')
	logging.debug('Method: ' + request.method)
	logging.debug('Endpoint Push: ' + str(Pushs.value))
	logging.debug('Endpoint Pop: ' + str(Pops.value))
	logging.debug('Endpoint Count: ' + str(Counts.value))
	logging.debug('Endpoint DeleteAll: ' + str(DeletesAll.value))
	logging.debug('Endpoint RedisHealth: ' + str(RedisHealths.value))
	Response = {'Pushs':Pushs.value, 'Pops':Pops.value, 'Counts':Counts.value, 'DeleteAll':DeletesAll.value, 'RedisHealth':RedisHealths.value}
	return jsonify(Response), 200

if __name__ == '__main__':
	redis_client = FlaskRedis(app)
	app.run(host = '0.0.0.0', port=int("8080"), debug=FlaskDebug) 
	# Debug se mantiene en True para que el error sea detallado al consumir la API.


from flask import Flask
from flask import jsonify, request
from datetime import datetime, timedelta
import numpy as np
from threading import Thread
import time


app = Flask(__name__)

# Pegando azoras pro server
horarioAtual = datetime.now()

hora = horarioAtual.hour
minuto = horarioAtual.minute
segundo = horarioAtual.second

# Atribuindo a hora atual para o relogio do servidor
relogioServidor = timedelta(hours=hora, minutes=minuto, seconds=segundo)

# Lista para armazenar os relogios
relogios = []

# Variavel para armazenar a media entre todos os relogios
media = {
    'hora': '0:0:0'
}

# Criando uma thread para atualizar a hora do servidor e tambem fazer o calculo para os relogios
def relogioServer():
	
	# Tornando as variaveis horario do servidor, lista de relogios e media global
	global relogioServidor
	global relogios
	global media
	
	# Loop infinito (muito tempo)
	while True:
		
		# Sleep de 1 segundo para poder adicionar 1 segundo ao relogio do servidor a cada 1 segundo
		time.sleep(1)
		relogioServidor = relogioServidor + timedelta(seconds=1)
		
		# Pegar todas as horas, minutos e segundos da lista de relogios cadastrados e fazer uma soma
		h = 0
		m = 0
		s = 0
		for r in relogios:
			aux = r.get('hora')
			aux = aux.split(":")
			h += int(aux[0])
			m += int(aux[1])
			s += int(aux[2])
		
		# Pegar as horas, minutos e segundos obtidos anteriormente e dividir pelo numero de relogios, para assim conseguir a media entre todos os relogios
		if len(relogios) != 0:
			#print(f"h = {h} - m = {m} - s = {s}")
			h = h / len(relogios)
			m = m / len(relogios)
			s = s / len(relogios)
			#print(f"Horas: {int(round(h,0))} - Minutos: {int(round(m,0))} - Segundos: {int(round(s,0))}")
			media = {
				'hora': f'{int(round(h,0))}:{int(round(m,0))}:{int(round(s,0))}'
			}
	
thread = Thread(target=relogioServer)
thread.start()

#relogioSincronizado = []

#horas = []
#minutos = []
#segundos = []

#server = str(relogioServidor)

#horas.append(int(server.split(':')[0]))
#minutos.append(int(server.split(':')[1]))
#segundos.append(int(server.split(':')[2]))

# Retorna todos os relogios
@app.route('/relogio/', methods=['GET'])
def retornaRelogios():
    return jsonify(relogios)


# Retorna um relogio em especifico
@app.route('/relogio/<int:id>', methods=['GET'])
def retornaRelogio(id):
	for relogio in relogios:
		if relogio.get('id') == int(id):
			return relogio
	return jsonify({"Error": "Relogio nao encontrado"})


# Retorna hora do server
@app.route('/relogio/server/', methods=['GET'])
def retornaServerTime():
	return jsonify({"ServerTime": f"{relogioServidor}"})


# Retorna a media do horario
@app.route('/relogio/media/', methods=['GET'])
def retornaMedia():
	return jsonify(media)


# Adiciona um relogio
# curl -i -H "Content-Type: application/json" -X POST -d '{"id": "666", "hora": "0:0:10"}' http://127.0.0.1:5000/relogio
@app.route('/relogio', methods=['POST'])
def adicionarRelogio():

    if not request.json:
        abort(400)
    relogio = {
		'id': int(request.json['id']),
		'hora': request.json['hora']
    }
    
    #hora = str(tempo['hora'])
    #horas.append(int(hora.split(':')[0]))
    #minutos.append(int(hora.split(':')[1]))
    #segundos.append(int(hora.split(':')[2]))
    
    relogios.append(relogio)
    
    return jsonify(relogios)


# Atualizar relogio cliente
# curl -i -H "Content-Type: application/json" -X PUT -d '{"id": "666", "hora": "17:10:30"}' http://127.0.0.1:5000/relogio/666
@app.route('/relogio/<int:id>', methods=['PUT'])
def atualizarRelogioCliente(id):
	for relogio in relogios:
		if relogio.get('id') == int(id):
			relogio.update({"hora": request.json['hora']})
			return jsonify({"Sucesso": "Relogio Atualizado"})
	return jsonify({"Error": "Relogio nao encontrado"})
    

#app.run(port=8080, host='10.141.115.7', debug=True)
app.run(debug=True)

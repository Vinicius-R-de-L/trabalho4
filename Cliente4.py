import random
import time
from datetime import datetime, timedelta
import requests
import PySimpleGUI as sg
from threading import Thread
import sys


# Código para definir elementos da interface
sg.theme("HotDogStand")

MainScreen = [
        [sg.Text('Hora com atrasos')],
        [sg.Text(key="hora_atual", text_color='black')],
		[sg.Text('Hora atualizada')],
		[sg.Text(key="hora_atualizada", text_color='black')],
]



# Id do cliente
id = 4


# Pegando azoras pro cliente
horarioAtual = datetime.now()

hora = horarioAtual.hour
minuto = horarioAtual.minute
segundo = horarioAtual.second

# Atribuindo a hora atual para o relogio do cliente
relogio = timedelta(hours=hora, minutes=minuto, seconds=segundo)


parametros = {
    'id': int(id),
    'hora': str(relogio)
}


# Url para usar a api, assim fica facil de trocar de localhost para outros
url = '127.0.0.1:5000'


# Variavel para quando o usuario fechar a interface grafica (thread principal) a thread tambem seja fechada
global fecharThread
fecharThread = False


# Adicionando o relogio ao servidor
requests.post(f'http://{url}/relogio', json=parametros)

def relogioCliente():
	
	# Tornando a variavel relogio global
    global relogio

	
    while True:
        if fecharThread:
            sys.exit()
        
        # Sleep de 1 segundo e adicionando + 1 segundo ao relogio     
        time.sleep(1)
        
        # Gerando um numero aleatorio para gerar os atrasos
        numeroAleatorio = random.randint(1, 10)
        
        if numeroAleatorio == 4:
            relogio = relogio + timedelta(minutes=1)
        elif numeroAleatorio == 8:
             relogio = relogio + timedelta(seconds=20)
        else:
            relogio = relogio + timedelta(seconds=1)
        
		# Atualizar relogio do cliente no servidor
        parametros = {
            'id': int(id),
            'hora': str(relogio)
        }
        
        # Atualizando o relogio no servidor
        requests.put(f'http://{url}/relogio/{id}', json=parametros)
        
        
        # Atualizar interface
        app['hora_atual'].update(str(relogio))
        
        
        # Pegando a hora atualizada do server
        response = requests.get(f'http://{url}/relogio/media/')
        response = response.json()
		
		# Atualizar interface
        app['hora_atualizada'].update(response['hora'])

thread = Thread(target=relogioCliente)
thread.start()

app = sg.Window("Relógio", MainScreen, finalize=True)

# Update na interface para mostrar o horario atual (para nao ter delay na interface na primeira execução)
app['hora_atual'].update(str(relogio))


# Loop para eventos da interface grafica
while True:

    event,values = app.read()

    
    if event == sg.WIN_CLOSED:
        fecharThread = True
        break

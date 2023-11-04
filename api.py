from flask import Flask, jsonify
from flask_cors import CORS
import readData

app = Flask(__name__)
CORS(app)

@app.route('/api/firstInFirstOut', methods=['GET'])
def getData():
    processes = readData.readJson()
    returnArr = []

    while (len(processes) > 0):
        process = processes.pop(0) # pegando e removendo o primeiro processo da fila
        ended = False # avisa que o processo ainda não foi finalizado

        # definir seu quantum
        quantum = process['quantum']

        # porcentagem de execução e tempo ocioso
        if process['type'] == 'cpu': # processo do tipo CPU
            execTime = quantum * 0.7 # 70 por cento será executado
            idleTime = quantum * 0.3 # 30 por cento será ocioso
        elif process['type'] == 'memory': # processo do tipo MEMÓRIA
            execTime = quantum * 0.6 # 60 por cento será executado
            idleTime = quantum * 0.4 # 30 por cento será ocioso
        else: # processo do tipo IO
            execTime = quantum * 0.5 # 50 por cento será executado
            idleTime = quantum * 0.5 # 30 por cento será ocioso

        # verificar se o quantum do processo é menor do que o tempo permitido para execução
        if process['time'] <= execTime: # significa que o processo será finalizado antes ou no instante da finalização de seu tempo total na iteração atual
            executionTime = process['time'] # execution time é o tempo restante de execução do processo
            idleTime = 0 # significa que o idle time na execução atual é 0
            ended = True # significa que o processo foi finalizado

            for i in processes:
                i['finalExecTime'] = i['finalExecTime'] + process['time'] # adiciona o tempo que o processo executou (sem ficar ocioso) em todos os outros processos

        else:
            # executionTime receberá o tempo de execução na iteração atual
            executionTime = execTime

            # remover de process['time'] execTime 
            process['time'] = process['time'] - execTime

            # adicionar execTime em todos os outros processos
            for i in processes:
                i['finalExecTime'] = i['finalExecTime'] + quantum

            # adicionar execTime no processo atual
            process['finalExecTime'] = process['finalExecTime'] + quantum

            # reinserir na fila
            processes.append(process)

        output = {
            'processID': process['idFIFO'], # retorna ao frontEnd a identificação do processo
            'executionTime': executionTime, # retorna ao frontEnd por quanto tempo o processo será executado na iteração atual
            'idleTime': idleTime, # retorna ao frontEnd por quanto tempo o processo ficará ocioso na iteração atual
            'totalQuantum': quantum, # retorna ao frontEnd por quanto tempo o processo ocupará a CPU (idleTime + executionTime)
            'ended': ended, # retorna ao frontEnd se o processo já foi finalizado, se ended = True, não deve mais ser inserido na fila
            'fullExecutionTime': process['finalExecTime'] # retorna por quanto tempo o processo já está em execução
        }

        returnArr.append(output) # insere o output no array de outputs, como se fossem logs

    return jsonify(returnArr) # envia ao frontend todo o log de execução

# @app.route('/api/fairShare', methods=['GET'])
# def getData():
#     teste = 1

# @app.route('/api/lottery', methods=['GET'])
# def getData():
#     teste = 1

# @app.route('/api/priorityQueues', methods=['GET'])
# def getData():
#     teste = 1

# @app.route('/api/shortestJobFirst', methods=['GET'])
# def getData():
#     teste = 1

if __name__ == '__main__':
    app.run(port = 3003)
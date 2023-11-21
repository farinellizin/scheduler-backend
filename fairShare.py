# Farinelli
import readData
import random

random.seed(42)

def defineQuantum(processesArr, type):
    cpuPercentage = 1 - (type ** len(processesArr))
    return cpuPercentage

def defineTenPercent(processesArr):
    for process in processesArr:
        process['tenPercent'] = int(0.1 * process['time'])

    return processesArr

def defineWeight(type):
    if type == 'cpu':
        return 0.7
    elif type == 'memory':
        return 0.6
    else:
        return 0.5

def clearOutput(output):
    output = {
        'processID': '',
        'action': '',
        'quantum': '',
        'processEnded': '',
        'execTimeIteration': '',
        'totalExecTime': '',
        'fullTimeInExecution': '',
        'processTimeRemaining': '',
        'idleTimeIteration': '',
        'totalIdleTime': ''
    }

    return output

def addFullExecutionTimeAllProcesses(processesArr, timeToAdd):
    for process in processesArr:
        process['finalExecTime'] = process['finalExecTime'] + timeToAdd

    return processesArr

def organizar_fila(fila):
    # Cria uma lista para armazenar tuplas (dicionário, frequência)
    frequencia = {}

    for elemento in fila:
        # Converte o dicionário para uma tupla ordenada para torná-lo hashable
        elemento_tupla = tuple(sorted(elemento.items()))
        frequencia[elemento_tupla] = frequencia.get(elemento_tupla, 0) + 1

    # Ordena os elementos com base em suas frequências
    fila_ordenada = []
    while frequencia:
        for elemento_tupla, count in sorted(frequencia.items()):
            for _ in range(count):
                fila_ordenada.append(dict(elemento_tupla))
            del frequencia[elemento_tupla]

    return fila_ordenada


processes = readData.readJson()
processes = defineTenPercent(processes)

filaCPUBound = ['1', '2', '3', '4', '5', '6', '7', '8']
filaIOBound = ['1', '2', '3', '4', '5']
filaMEMORYBound = ['1', '2', '3', '4', '5', '6', '7']

action = ""
output = {
    'processID': '',
    'action': '',
    'quantum': '',
    'processEnded': '',
    'execTimeIteration': '',
    'totalExecTime': '',
    'fullTimeInExecution': '',
    'processTimeRemaining': '',
    'idleTimeIteration': '',
    'totalIdleTime': '',
    'user_id': ''
}

returnArr = []
actionHappened = False


for process in processes:
    print(process['user_id'])

processes = organizar_fila(processes)
print()
print()

for process in processes:
    print(process['user_id'])

# while (len(processes) > 0):
#     # ordenar a fila
    
#     processes.pop(0)
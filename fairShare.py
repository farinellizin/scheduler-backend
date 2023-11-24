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

def equalizeUsers(vetor):
    segundo_vetor = []

    while len(vetor) > 0:
        for valor in range(1, 5):
            for item in vetor:
                if item['user_id'] == valor:
                    segundo_vetor.append(item)
                    vetor.remove(item)
                    break

    return segundo_vetor

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

processes = equalizeUsers(processes)


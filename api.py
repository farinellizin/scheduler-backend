from flask import Flask, jsonify, request
from flask_cors import CORS
import readData
import random
import json
random.seed(42)

def defineQuantum(processesArr, type):
    cpuPercentage = 1 - (type ** len(processesArr))
    return cpuPercentage

def defineTenPercent(processesArr):
    for process in processesArr:
        process['tenPercent'] = int(0.1 * process['time'])

    return processesArr

def defineWeight(type, weightArr):
    if type == 'cpu':
        if weightArr[0] != 0:
            return weightArr[0]
        else:
            return 0.7
    elif type == 'memory':
        if weightArr[1] != 0:
            return weightArr[1]
        else:
            return 0.6
    else:
        if weightArr[2] != 0:
            return weightArr[2]
        else:
            return 0.5

def clearOutput(output):
    output = {
        'processID': '',
        'priority': '',
        'action': '',
        'quantum': '',
        'processEnded': '',
        'execTimeIteration': '',
        'totalExecTime': '',
        'fullTimeInExecution': '',
        'processTimeRemaining': '',
        'idleTimeIteration': '',
        'totalIdleTime': '',
        'user_id': '',
        'winnerTicket': ''
    }

    return output

def addFullExecutionTimeAllProcesses(processesArr, timeToAdd):
    for process in processesArr:
        process['finalExecTime'] = process['finalExecTime'] + timeToAdd

    return processesArr

def readProcessesFromUser(dataSetJson):
    dataSetJson = json.loads(dataSetJson)
    filaCPUBound = []
    filaMEMORYBound = []
    filaIOBound = []
    processes = []
    i = 1

    for processo in dataSetJson:
        process = {
            'type': processo['type'],
            'time': processo['time'],
            'priority': processo['priority'],
            'idFIFO': i,
            'finalExecTime': 0,
            'user_id': processo['user_id']
        }

        if processo['type'] == 'cpu':
            filaCPUBound.append(1)
        elif processo['type'] == 'memory':
            filaMEMORYBound.append(1)
        else:
            filaIOBound.append(1)

        processes.append(process)
        i = i + 1

    return processes, filaCPUBound, filaMEMORYBound, filaIOBound

def hashingTickets(sortedTickets, process, tickets):
    for t in tickets:
        sortedTickets.append({t: process})

def spreadRandomTickets(sortedTickets, processes):
    ticketsList = list(range(1, 101))

    for p in processes:
        tickets = random.sample(ticketsList, k = random.randint(1, 5))
        ticketsList = list(set(ticketsList) - set(tickets))
        hashingTickets(sortedTickets, p, tickets)
        p['tickets'] = tickets


def spreadEqualTickets(sortedTickets, processes):
    ticketsList = list(range(1, 101))

    for p in processes:
        tickets = random.sample(ticketsList, 5)
        ticketsList = list(set(ticketsList) - set(tickets))
        hashingTickets(sortedTickets, p, tickets)
        p['tickets'] = tickets


def spreadPriorityTickets(sortedTickets, processes):
    ticketsList = list(range(1, 101))

    for p in processes:
        tickets = random.sample(ticketsList, defineTicketsByPriority(p['priority']))
        ticketsList = list(set(ticketsList) - set(tickets))
        hashingTickets(sortedTickets, p, tickets)
        p['tickets'] = tickets


def defineTicketsByPriority(priority):
    if priority == 1: return 10
    elif priority == 2: return 8
    elif priority == 3: return 6
    elif priority == 4: return 4
    else: return 2

def chooseTypeOfSpreading(sortedTickets, processes, lottery):
    if lottery == "random": spreadRandomTickets(sortedTickets, processes)
    elif lottery == "equal": spreadEqualTickets(sortedTickets, processes)
    else: spreadPriorityTickets(sortedTickets, processes)

def chooseWinnerProcess(sortedTickets):
    sortedDict = random.choice(sortedTickets)
    listKeys = list(sortedDict.keys())

    winnerTicket = listKeys[0]
    process = sortedDict[winnerTicket]

    return process, winnerTicket

def deleteEndedTickets(sortedTickets, tickets):
    for t in tickets:
        del sortedTickets[next(i for i,d in enumerate(sortedTickets) if t in d)]
       
def equalizeUsers(processes):
    returnArrProcesses = []

    while len(processes) > 0:
        for valor in range(1, 5):
            for item in processes:
                if item['user_id'] == valor:
                    returnArrProcesses.append(item)
                    processes.remove(item)
                    break

    return returnArrProcesses

def sortProcessesByTime(processesArr):
    processesArr.sort(key=lambda x: x['time'])
    return processesArr


app = Flask(__name__)
CORS(app)

@app.route('/api/firstInFirstOut/<int:from_value>/<int:to_value>/<float:cpu_weight>/<float:memory_weight>/<float:io_weight>/<string:dataSet>', methods=['GET'])
def getDataFirstInFirstOut(from_value, to_value, cpu_weight, memory_weight, io_weight, dataSet):
    weightArr = [cpu_weight, memory_weight, io_weight]

    if from_value == 0:
        from_value = 10

    if to_value == 0:
        to_value = 30

    if dataSet != '0':
        processes, filaCPUBound, filaMEMORYBound, filaIOBound = readProcessesFromUser(dataSet)
    else:
        processes = readData.readJson()
        filaCPUBound = ['1', '2', '3', '4', '5', '6', '7', '8']
        filaIOBound = ['1', '2', '3', '4', '5']
        filaMEMORYBound = ['1', '2', '3', '4', '5', '6', '7']

    processes = defineTenPercent(processes)

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

    # * Primeiro Looping
    while (len(processes) > 0):
        # 1
        process = processes.pop(0)

        # 1.5
        weight = defineWeight(process['type'], weightArr)

        # 2 
        if process['time'] <= process['tenPercent']:
            quantum = process['tenPercent']
        else:
            quantum = int(process['time'] * (1 + float(f'0.{random.randint(from_value, to_value)}')))

        # 3
        if process['type'] == 'cpu':
            execTime = max(0, int(quantum * defineQuantum(filaCPUBound, weight)))
        elif process['type'] == 'memory':
            execTime = max(0, int(quantum * defineQuantum(filaMEMORYBound, weight)))
        else:
            execTime = max(0, int(quantum * defineQuantum(filaIOBound, weight)))

        idleTime = quantum - execTime

        # 4
        key = 2

        # * Segundo Looping
        while quantum > 0 and process['time'] > 0:
            i = 0
            output = clearOutput(output)

            if (key % 2) == 0 and execTime > 0:
                i = i + 1
                action = 'execute'
                actionHappened = True

                if process['time'] == 1 or execTime == 1:
                    variableExecTime = 1
                elif process['time'] <= process['tenPercent']:
                    variableExecTime = max(0, int(process['time'] / 2))
                elif execTime >= process['time']:
                    variableExecTime = random.randint(1, process['time'])
                elif execTime < process['time']:
                    variableExecTime = random.randint(1, execTime)

                process['time'] = max(0, process['time'] - variableExecTime)
                quantum = max(0, quantum - variableExecTime)
                execTime = max(0, execTime - variableExecTime)

                process['finalExecTime'] = process['finalExecTime'] + variableExecTime
                addFullExecutionTimeAllProcesses(processes, variableExecTime)

                output = {
                    'processID': process['idFIFO'],
                    'action': action,
                    'quantum': quantum,
                    'processEnded': '',
                    'execTimeIteration': variableExecTime,
                    'totalExecTime': execTime,
                    'fullTimeInExecution': process['finalExecTime'],
                    'processTimeRemaining': process['time'],
                    'idleTimeIteration': '',
                    'totalIdleTime': '',
                    'user_id': ''
                }
                
            # 6
            elif (key % 2) != 0 and idleTime > 0:
                i = i + 1
                action = 'idle'
                actionHappened = True

                if idleTime == 1:
                    variableIdleTime = 1
                elif idleTime > 1:
                    variableIdleTime = random.randint(1, idleTime)

                quantum = max(0, quantum - variableIdleTime)
                idleTime = max(0, idleTime - variableIdleTime)

                process['finalExecTime'] = process['finalExecTime'] + variableIdleTime
                addFullExecutionTimeAllProcesses(processes, variableIdleTime)

                output = {
                    'processID': process['idFIFO'],
                    'action': action,
                    'quantum': quantum,
                    'processEnded': '',
                    'execTimeIteration': '',
                    'totalExecTime': '',
                    'fullTimeInExecution': process['finalExecTime'],
                    'processTimeRemaining': process['time'],
                    'idleTimeIteration': variableIdleTime,
                    'totalIdleTime': idleTime,
                    'user_id': ''
                }

            if process['time'] != 0:
                processEnded = False
            else:
                processEnded = True

            output['processEnded'] = processEnded

            if actionHappened:
                returnArr.append(output)
            
            actionHappened = False

            key = random.randint(1, 2)

        # 7
        if process['time'] != 0:
            processes.append(process)
        else:
            if process['type'] == 'cpu':
                filaCPUBound.pop()
            elif process['type'] == 'memory':
                filaMEMORYBound.pop()
            else:
                filaIOBound.pop()

    return jsonify(returnArr) # envia ao frontend todo o log de execução

@app.route('/api/fairShare/<int:from_value>/<int:to_value>/<float:cpu_weight>/<float:memory_weight>/<float:io_weight>/<string:dataSet>', methods=['GET'])
def getDataFairShare(from_value, to_value, cpu_weight, memory_weight, io_weight, dataSet):
    weightArr = [cpu_weight, memory_weight, io_weight]

    if from_value == 0:
        from_value = 10

    if to_value == 0:
        to_value = 30

    if dataSet != '0':
        processes, filaCPUBound, filaMEMORYBound, filaIOBound = readProcessesFromUser(dataSet)
    else:
        processes = readData.readJson()
        filaCPUBound = ['1', '2', '3', '4', '5', '6', '7', '8']
        filaIOBound = ['1', '2', '3', '4', '5']
        filaMEMORYBound = ['1', '2', '3', '4', '5', '6', '7']

    processes = defineTenPercent(processes)
    processes = equalizeUsers(processes)

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

    # * Primeiro Looping
    while (len(processes) > 0):
        # 1
        process = processes.pop(0)

        # 1.5
        weight = defineWeight(process['type'], weightArr)

        # 2 
        if process['time'] <= process['tenPercent']:
            quantum = process['tenPercent']
        else:
            quantum = int(process['time'] * (1 + float(f'0.{random.randint(from_value, to_value)}')))

        # 3
        if process['type'] == 'cpu':
            execTime = max(0, int(quantum * defineQuantum(filaCPUBound, weight)))
        elif process['type'] == 'memory':
            execTime = max(0, int(quantum * defineQuantum(filaMEMORYBound, weight)))
        else:
            execTime = max(0, int(quantum * defineQuantum(filaIOBound, weight)))

        idleTime = quantum - execTime

        # 4
        key = 2

        # * Segundo Looping
        while quantum > 0 and process['time'] > 0:
            i = 0
            output = clearOutput(output)

            if (key % 2) == 0 and execTime > 0:
                i = i + 1
                action = 'execute'
                actionHappened = True

                if process['time'] == 1 or execTime == 1:
                    variableExecTime = 1
                elif process['time'] <= process['tenPercent']:
                    variableExecTime = max(0, int(process['time'] / 2))
                elif execTime >= process['time']:
                    variableExecTime = random.randint(1, process['time'])
                elif execTime < process['time']:
                    variableExecTime = random.randint(1, execTime)

                process['time'] = max(0, process['time'] - variableExecTime)
                quantum = max(0, quantum - variableExecTime)
                execTime = max(0, execTime - variableExecTime)

                process['finalExecTime'] = process['finalExecTime'] + variableExecTime
                addFullExecutionTimeAllProcesses(processes, variableExecTime)

                output = {
                    'processID': process['idFIFO'],
                    'action': action,
                    'quantum': quantum,
                    'processEnded': '',
                    'execTimeIteration': variableExecTime,
                    'totalExecTime': execTime,
                    'fullTimeInExecution': process['finalExecTime'],
                    'processTimeRemaining': process['time'],
                    'idleTimeIteration': '',
                    'totalIdleTime': '',
                    'user_id': process['user_id']
                }
                
            # 6
            elif (key % 2) != 0 and idleTime > 0:
                i = i + 1
                action = 'idle'
                actionHappened = True

                if idleTime == 1:
                    variableIdleTime = 1
                elif idleTime > 1:
                    variableIdleTime = random.randint(1, idleTime)

                quantum = max(0, quantum - variableIdleTime)
                idleTime = max(0, idleTime - variableIdleTime)

                process['finalExecTime'] = process['finalExecTime'] + variableIdleTime
                addFullExecutionTimeAllProcesses(processes, variableIdleTime)

                output = {
                    'processID': process['idFIFO'],
                    'action': action,
                    'quantum': quantum,
                    'processEnded': '',
                    'execTimeIteration': '',
                    'totalExecTime': '',
                    'fullTimeInExecution': process['finalExecTime'],
                    'processTimeRemaining': process['time'],
                    'idleTimeIteration': variableIdleTime,
                    'totalIdleTime': idleTime,
                    'user_id': process['user_id']
                }

            if process['time'] != 0:
                processEnded = False
            else:
                processEnded = True

            output['processEnded'] = processEnded

            if actionHappened:
                returnArr.append(output)
            
            actionHappened = False

            key = random.randint(1, 2)

        # 7
        if process['time'] != 0:
            processes.append(process)
        else:
            if process['type'] == 'cpu':
                filaCPUBound.pop()
            elif process['type'] == 'memory':
                filaMEMORYBound.pop()
            else:
                filaIOBound.pop()

    return jsonify(returnArr) # envia ao frontend todo o log de execução

@app.route('/api/lottery/<int:from_value>/<int:to_value>/<float:cpu_weight>/<float:memory_weight>/<float:io_weight>/<string:dataSet>/<string:lotteryType>', methods=['GET'])
def getDataLottery(from_value, to_value, cpu_weight, memory_weight, io_weight, dataSet, lotteryType):
   
    weightArr = [cpu_weight, memory_weight, io_weight]

    sortedTickets = []

    if from_value == 0:
        from_value = 10

    if to_value == 0:
        to_value = 30

    if dataSet != '0':
        processes, filaCPUBound, filaMEMORYBound, filaIOBound = readProcessesFromUser(dataSet)
    else:
        processes = readData.readJson()
        filaCPUBound = ['1', '2', '3', '4', '5', '6', '7', '8']
        filaIOBound = ['1', '2', '3', '4', '5']
        filaMEMORYBound = ['1', '2', '3', '4', '5', '6', '7']

    processes = defineTenPercent(processes)

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
        'user_id': '',
        'winnerTicket': ''
    }

    returnArr = []
    actionHappened = False

    chooseTypeOfSpreading(sortedTickets, processes, lotteryType)

    while (len(processes) > 0):
        # 1
        process, winnerTicket = chooseWinnerProcess(sortedTickets)

        for p in processes:
            if p['idFIFO'] == process['idFIFO']:
                processes.remove(p)

        # 1.5
        weight = defineWeight(process['type'], weightArr)

        # 2 
        if process['time'] <= process['tenPercent']:
            quantum = process['tenPercent']
        else:
            quantum = int(process['time'] * (1 + float(f'0.{random.randint(from_value, to_value)}')))

        # 3
        if process['type'] == 'cpu':
            execTime = max(0, int(quantum * defineQuantum(filaCPUBound, weight)))
        elif process['type'] == 'memory':
            execTime = max(0, int(quantum * defineQuantum(filaMEMORYBound, weight)))
        else:
            execTime = max(0, int(quantum * defineQuantum(filaIOBound, weight)))

        idleTime = quantum - execTime

        # 4
        key = 2

    # * Segundo Looping
        while quantum > 0 and process['time'] > 0:
            i = 0
            output = clearOutput(output)

            if (key % 2) == 0 and execTime > 0:
                i = i + 1
                action = 'execute'
                actionHappened = True

                if process['time'] == 1 or execTime == 1:
                    variableExecTime = 1
                elif process['time'] <= process['tenPercent']:
                    variableExecTime = max(0, int(process['time'] / 2))
                elif execTime >= process['time']:
                    variableExecTime = random.randint(1, process['time'])
                elif execTime < process['time']:
                    variableExecTime = random.randint(1, execTime)

                process['time'] = max(0, process['time'] - variableExecTime)
                quantum = max(0, quantum - variableExecTime)
                execTime = max(0, execTime - variableExecTime)

                process['finalExecTime'] = process['finalExecTime'] + variableExecTime
                addFullExecutionTimeAllProcesses(processes, variableExecTime)

                output = {
                    'processID': process['idFIFO'],
                    'action': action,
                    'quantum': quantum,
                    'processEnded': '',
                    'execTimeIteration': variableExecTime,
                    'totalExecTime': execTime,
                    'fullTimeInExecution': process['finalExecTime'],
                    'processTimeRemaining': process['time'],
                    'idleTimeIteration': '',
                    'totalIdleTime': '',
                    'user_id': '',
                    'winnerTicket': winnerTicket
                }
                
            # 6
            elif (key % 2) != 0 and idleTime > 0:
                i = i + 1
                action = 'idle'
                actionHappened = True

                if idleTime == 1:
                    variableIdleTime = 1
                elif idleTime > 1:
                    variableIdleTime = random.randint(1, idleTime)

                quantum = max(0, quantum - variableIdleTime)
                idleTime = max(0, idleTime - variableIdleTime)

                process['finalExecTime'] = process['finalExecTime'] + variableIdleTime
                addFullExecutionTimeAllProcesses(processes, variableIdleTime)

                output = {
                    'processID': process['idFIFO'],
                    'action': action,
                    'quantum': quantum,
                    'processEnded': '',
                    'execTimeIteration': '',
                    'totalExecTime': '',
                    'fullTimeInExecution': process['finalExecTime'],
                    'processTimeRemaining': process['time'],
                    'idleTimeIteration': variableIdleTime,
                    'totalIdleTime': idleTime,
                    'user_id': '',
                    'winnerTicket': winnerTicket
                }

            if process['time'] != 0:
                processEnded = False
            else:
                deleteEndedTickets(sortedTickets, process['tickets'])
                processEnded = True

            output['processEnded'] = processEnded

            if actionHappened:
                returnArr.append(output)
            
            actionHappened = False

            key = random.randint(1, 2)

        # 7
        if process['time'] != 0:

            processes.append(process)

        else:
            if process['type'] == 'cpu':
                filaCPUBound.pop()
            elif process['type'] == 'memory':
                filaMEMORYBound.pop()
            else:
                filaIOBound.pop()


    return jsonify(returnArr)

@app.route('/api/priorityQueues/<int:from_value>/<int:to_value>/<float:cpu_weight>/<float:memory_weight>/<float:io_weight>/<string:dataSet>', methods=['GET'])
def getDataPQ(from_value, to_value, cpu_weight, memory_weight, io_weight, dataSet):
    weightArr = [cpu_weight, memory_weight, io_weight]

    if from_value == 0:
        from_value = 10

    if to_value == 0:
        to_value = 30

    if dataSet != '0':
        processes, filaCPUBound, filaMEMORYBound, filaIOBound = readProcessesFromUser(dataSet)
    else:
        processes = readData.readJson()
        filaCPUBound = ['1', '2', '3', '4', '5', '6', '7', '8']
        filaIOBound = ['1', '2', '3', '4', '5']
        filaMEMORYBound = ['1', '2', '3', '4', '5', '6', '7']

    processes = defineTenPercent(processes)
    processes = sorted(processes, key=lambda x: x['priority'])

    action = ""
    output = {
        'processID': '',
        'priority': '',
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

    returnArr = []
    actionHappened = False

    # * Primeiro Looping
    while (len(processes) > 0):
        # 1
        process = processes.pop(0)

        # 1.5
        weight = defineWeight(process['type'], weightArr)

        # 2 
        if process['time'] <= process['tenPercent']:
            quantum = process['tenPercent']
        else:
            quantum = int(process['time'] * (1 + float(f'0.{random.randint(from_value, to_value)}')))

        # 3
        if process['type'] == 'cpu':
            execTime = max(0, int(quantum * defineQuantum(filaCPUBound, weight)))
        elif process['type'] == 'memory':
            execTime = max(0, int(quantum * defineQuantum(filaMEMORYBound, weight)))
        else:
            execTime = max(0, int(quantum * defineQuantum(filaIOBound, weight)))

        idleTime = quantum - execTime

        # 4
        key = 2

        # * Segundo Looping
        while quantum > 0 and process['time'] > 0:
            i = 0
            output = clearOutput(output)

            if (key % 2) == 0 and execTime > 0:
                i = i + 1
                action = 'execute'
                actionHappened = True

                if process['time'] == 1 or execTime == 1:
                    variableExecTime = 1
                elif process['time'] <= process['tenPercent']:
                    variableExecTime = max(0, int(process['time'] / 2))
                elif execTime >= process['time']:
                    variableExecTime = random.randint(1, process['time'])
                elif execTime < process['time']:
                    variableExecTime = random.randint(1, execTime)

                process['time'] = max(0, process['time'] - variableExecTime)
                quantum = max(0, quantum - variableExecTime)
                execTime = max(0, execTime - variableExecTime)

                process['finalExecTime'] = process['finalExecTime'] + variableExecTime
                addFullExecutionTimeAllProcesses(processes, variableExecTime)

                output = {
                    'processID': process['idFIFO'],
                    'priority': process['priority'],
                    'action': action,
                    'quantum': quantum,
                    'processEnded': '',
                    'execTimeIteration': variableExecTime,
                    'totalExecTime': execTime,
                    'fullTimeInExecution': process['finalExecTime'],
                    'processTimeRemaining': process['time'],
                    'idleTimeIteration': '',
                    'totalIdleTime': ''
                }
                
            # 6
            elif (key % 2) != 0 and idleTime > 0:
                i = i + 1
                action = 'idle'
                actionHappened = True

                if idleTime == 1:
                    variableIdleTime = 1
                elif idleTime > 1:
                    variableIdleTime = random.randint(1, idleTime)

                quantum = max(0, quantum - variableIdleTime)
                idleTime = max(0, idleTime - variableIdleTime)

                process['finalExecTime'] = process['finalExecTime'] + variableIdleTime
                addFullExecutionTimeAllProcesses(processes, variableIdleTime)

                output = {
                    'processID': process['idFIFO'],
                    'priority': process['priority'],
                    'action': action,
                    'quantum': quantum,
                    'processEnded': '',
                    'execTimeIteration': '',
                    'totalExecTime': '',
                    'fullTimeInExecution': process['finalExecTime'],
                    'processTimeRemaining': process['time'],
                    'idleTimeIteration': variableIdleTime,
                    'totalIdleTime': idleTime
                }

            if process['time'] != 0:
                processEnded = False
            else:
                processEnded = True

            output['processEnded'] = processEnded

            if actionHappened:
                returnArr.append(output)
            
            actionHappened = False

            key = random.randint(1, 2)

        # 7
        if process['time'] != 0:
            processes.insert(0, process)
        else:
            if process['type'] == 'cpu':
                filaCPUBound.pop()
            elif process['type'] == 'memory':
                filaMEMORYBound.pop()
            else:
                filaIOBound.pop()

    return jsonify(returnArr)

@app.route('/api/shortestJobFirst/<int:from_value>/<int:to_value>/<float:cpu_weight>/<float:memory_weight>/<float:io_weight>/<string:dataSet>', methods=['GET'])
def getDataShortestJobFirst(from_value, to_value, cpu_weight, memory_weight, io_weight, dataSet):
    weightArr = [cpu_weight, memory_weight, io_weight]

    if from_value == 0:
        from_value = 10

    if to_value == 0:
        to_value = 30

    if dataSet != '0':
        processes, filaCPUBound, filaMEMORYBound, filaIOBound = readProcessesFromUser(dataSet)
    else:
        processes = readData.readJson()
        filaCPUBound = ['1', '2', '3', '4', '5', '6', '7', '8']
        filaIOBound = ['1', '2', '3', '4', '5']
        filaMEMORYBound = ['1', '2', '3', '4', '5', '6', '7']

    processes = defineTenPercent(processes)

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
        'totalIdleTime': ''
    }

    returnArr = []
    actionHappened = False

    # * Primeiro Looping
    while (len(processes) > 0):
        # 1
        processes = sortProcessesByTime(processes)
        process = processes.pop(0)

        # 1.5
        weight = defineWeight(process['type'], weightArr)

        # 2 
        if process['time'] <= process['tenPercent']:
            quantum = process['tenPercent']
        else:
            quantum = int(process['time'] * (1 + float(f'0.{random.randint(10, 30)}')))

        # 3
        if process['type'] == 'cpu':
            execTime = max(0, int(quantum * defineQuantum(filaCPUBound, weight)))
        elif process['type'] == 'memory':
            execTime = max(0, int(quantum * defineQuantum(filaMEMORYBound, weight)))
        else:
            execTime = max(0, int(quantum * defineQuantum(filaIOBound, weight)))

        idleTime = quantum - execTime

        # 4
        key = 2

        # * Segundo Looping
        while quantum > 0 and process['time'] > 0:
            i = 0
            output = clearOutput(output)

            if (key % 2) == 0 and execTime > 0:
                i = i + 1
                action = 'execute'
                actionHappened = True

                if process['time'] == 1 or execTime == 1:
                    variableExecTime = 1
                elif process['time'] <= process['tenPercent']:
                    variableExecTime = max(0, int(process['time'] / 2))
                elif execTime >= process['time']:
                    variableExecTime = random.randint(1, process['time'])
                elif execTime < process['time']:
                    variableExecTime = random.randint(1, execTime)

                process['time'] = max(0, process['time'] - variableExecTime)
                quantum = max(0, quantum - variableExecTime)
                execTime = max(0, execTime - variableExecTime)

                process['finalExecTime'] = process['finalExecTime'] + variableExecTime
                addFullExecutionTimeAllProcesses(processes, variableExecTime)

                output = {
                    'processID': process['idFIFO'],
                    'action': action,
                    'quantum': quantum,
                    'processEnded': '',
                    'execTimeIteration': variableExecTime,
                    'totalExecTime': execTime,
                    'fullTimeInExecution': process['finalExecTime'],
                    'processTimeRemaining': process['time'],
                    'idleTimeIteration': '',
                    'totalIdleTime': ''
                }
                
            # 6
            elif (key % 2) != 0 and idleTime > 0:
                i = i + 1
                action = 'idle'
                actionHappened = True

                if idleTime == 1:
                    variableIdleTime = 1
                elif idleTime > 1:
                    variableIdleTime = random.randint(1, idleTime)

                quantum = max(0, quantum - variableIdleTime)
                idleTime = max(0, idleTime - variableIdleTime)

                process['finalExecTime'] = process['finalExecTime'] + variableIdleTime
                addFullExecutionTimeAllProcesses(processes, variableIdleTime)

                output = {
                    'processID': process['idFIFO'],
                    'action': action,
                    'quantum': quantum,
                    'processEnded': '',
                    'execTimeIteration': '',
                    'totalExecTime': '',
                    'fullTimeInExecution': process['finalExecTime'],
                    'processTimeRemaining': process['time'],
                    'idleTimeIteration': variableIdleTime,
                    'totalIdleTime': idleTime
                }

            if process['time'] != 0:
                processEnded = False
            else:
                processEnded = True

            output['processEnded'] = processEnded

            if actionHappened:
                returnArr.append(output)
            
            actionHappened = False

            key = random.randint(1, 2)

        # 7
        if process['time'] != 0:
            processes.append(process)
        else:
            if process['type'] == 'cpu':
                filaCPUBound.pop()
            elif process['type'] == 'memory':
                filaMEMORYBound.pop()
            else:
                filaIOBound.pop()

    return jsonify(returnArr)

if __name__ == '__main__':
    app.run(port = 3001)
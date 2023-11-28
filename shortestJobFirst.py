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



def sortProcessesByTime(processesArr):
    processesArr.sort(key=lambda x: x['time'])
    return processesArr






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
    weight = defineWeight(process['type'])

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
            print(output)
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
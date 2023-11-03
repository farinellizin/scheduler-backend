import json

def readJson():
    processesArr = []
    jsonFilesArr = ['cpuBound.json', 'ioBound.json', 'memoryBound.json']
    i = 1

    for fileName in jsonFilesArr:
        with open(f'./data/{fileName}', 'r') as json_content:
            dados = json.load(json_content)

            for processo in dados['processes']:
                process = {
                    'type': processo['type'],
                    'time': processo['time'],
                    'priority': processo['priority'],
                    'quantum': (processo['time'] * 1.1),
                    'idFIFO': i,
                    'finalExecTime': processo['execTime']
                }

                processesArr.append(process)
                i = i + 1

    return processesArr
import numpy as np

def create_valueation_matrix(datafile):
    #input come in the form agent_id, resouce_id, value
    agents = []
    resource = []
    value = []
    with open(datafile,'r') as file:
        lines = file.read().split("\n")
        for i in range(len(lines)-1):
            line = lines[i].split(', ')
            agents.append(line[0])
            resource.append(line[1])
            value.append(line[2])
    
    uniqueAgents = len(set(agents))
    uniqueResource = len(set(resource))

    valueationMatrix = np.zeros([uniqueAgents,uniqueResource])

    for i in range(len(value)):
        x = int(i / uniqueResource)
        y = i % uniqueResource
        if int(value[i]) == 0:
            valueationMatrix[x,y] = 1
        else: 
            valueationMatrix[x,y] = value[i]

    return valueationMatrix

create_valueation_matrix("/home/jens/Skrivebord/F2022/bachelor/EFX-algo/RealData/realData18")
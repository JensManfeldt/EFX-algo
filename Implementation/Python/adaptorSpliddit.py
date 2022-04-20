import numpy as np

def create_valueation_matrix(datafile):
    #input come in the form agent_id, resouce_id, value
    with open(datafile,'r') as file:
        lines = file.read().split("\n")
        for i in range(len(lines)-1):
            line = lines[i].split(', ')
            print(line)


    #return valueationMatrix

create_valueation_matrix("/home/jens/Skrivebord/F2022/bachelor/EFX-algo/RealData/realData18")
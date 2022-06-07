import numpy as np
import util as u
import adaptorSpliddit
import os

dataPath = "/home/jens/Skrivebord/F2022/bachelor/EFX-algo/RealData/realData"

class Brute:

    def __init__(self, numAgents, numItems, agentsValuations):
        self.bestNashSoFor = -1
        self.bestAlloc = np.zeros([numAgents,numItems])
        self.agentsValuations = agentsValuations
        self.itemArray = np.zeros(numItems, dtype=int)
        self.numAgent = numAgents


    def findOptimalNash(self):
        self.tryAllValues(0)
        return self.bestAlloc, self.bestNashSoFor

    def tryAllValues(self, index):
        
        for i in range(self.numAgent):
            self.itemArray[index] = i
            if index != len(self.itemArray) - 1:   
                self.tryAllValues(index + 1)
            else :
                bundleAssignment = np.zeros(self.agentsValuations.shape)
                for i in range(len(self.itemArray)):
                    bundleAssignment[self.itemArray[i],i] = 1
                nashForBundle = self.calcNashWelFare(self.agentsValuations, bundleAssignment)
                if nashForBundle > self.bestNashSoFor:
                    self.bestNashSoFor = nashForBundle
                    self.bestAlloc = bundleAssignment


    def calcNashWelFare(self, agentsEvaluations, bundleAssignment):
        welFare = 1
        n = agentsEvaluations.shape[0]
        #print("Agents Eval")
        #print(agentsEvaluations)
        #print("Bundle Assign")
        #print(bundleAssignment)
        for i in range(n):
            agentValueation = sum(agentsEvaluations[i,:] * bundleAssignment[i,:])
            #print("Agent : " + str(i) + " valueation is : " + str(agentValueation))
            agentValueation = pow(agentValueation,1/n)
            
            welFare *= agentValueation

        return welFare


dataPath = "/home/jens/Skrivebord/F2022/bachelor/EFX-algo/RealData/"
savePath = "/home/jens/Skrivebord/F2022/bachelor/EFX-algo/optimalNashAllocSpliddit/"
solvedWrong = ['79362','16585','54101','33729','56989','15810','31292','6518','53473','57815','15466','64536','53489','32484','9474','65533','3235','32723','1675','1105','4866','53471','30542','31422','33732','32490','6608','28512','53476','4435','53479','30543','70824','76342','3023','53346']
for file in os.listdir(dataPath):
#for file in solvedWrong:

    valueationMatrix = adaptorSpliddit.create_valueation_matrix(dataPath + str(file))
    problemTime = pow(valueationMatrix.shape[0],valueationMatrix.shape[1])
    print("Working on problem " + str(file) + " with size :" + str(problemTime))
    if problemTime >= 20000000:
        print("Problem " + str(file) + " to big")
        continue
    b = Brute(valueationMatrix.shape[0],valueationMatrix.shape[1],valueationMatrix)
    alloc, bestNash = b.findOptimalNash()
    u.saveOptimalAlloction(file,alloc,bestNash, savePath)



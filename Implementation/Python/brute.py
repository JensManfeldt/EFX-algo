import numpy as np
import util as u

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

        for i in range(n):
            agentValueation = sum(agentsEvaluations[i,:] * bundleAssignment[i,:])
            agentValueation = pow(agentValueation,1/n)
            
            welFare *= agentValueation

        return welFare




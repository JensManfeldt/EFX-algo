import adaptorSpliddit
import efxSolver
import os
import numpy as np

realdataPath = "/home/jens/Skrivebord/F2022/bachelor/EFX-algo/RealData/"

demoDataPath = "/home/jens/Skrivebord/F2022/bachelor/EFX-algo/DempoData/"

dataPath = demoDataPath

def generateBundleAssignmentWithDraft(agentsValueations):
    copy = np.matrix.copy(agentsValueations)
    bundleAssignement = np.zeros([agentsValueations.shape[0],agentsValueations.shape[1]], dtype=int)
    for j in range(agentsValueations.shape[1]):
        agentToPick = j % agentsValueations.shape[0]

        bestItem = int(np.argmax(copy[agentToPick,:]))
        bundleAssignement[agentToPick,bestItem] = 1

        copy[:,bestItem] = -1

    return bundleAssignement

def calcNashWellFare(agentsEvaluations, bundleAssignment):

    welFare = 1
    n = agentsEvaluations.shape[0]

    for i in range(n):
        #print(bundleAssignment.shape)
        agentValueation = sum(agentsEvaluations[i,:] * bundleAssignment[i,:])
        #print("Agent : " + str(i) + " valueation is : " + str(agentValueation))
        
        agentValueation = pow(agentValueation,1/n)
        
        welFare *= agentValueation

    return welFare

def isAllocEFX(alloc,agentsValueations):
    for i in range(agentsValueations.shape[0]):
        valueOfAssignedBundle = sum(alloc[i,:] * agentsValueations[i,:])
        for j in range(agentsValueations.shape[0]):
            agentsEvalOfBundle = alloc[j,:] * agentsValueations[i,]
            nonZeroIndexs = np.nonzero(agentsEvalOfBundle)
            withoutZeros = agentsEvalOfBundle[nonZeroIndexs]
            if len(withoutZeros) == 0:
                continue
            else :
                leastValuedItem = np.min(withoutZeros)
            if valueOfAssignedBundle < sum(agentsEvalOfBundle) - leastValuedItem:
                return False
    
    return True



for file in os.listdir(dataPath):
    valueationMatrix = adaptorSpliddit.create_valueation_matrix(dataPath + str(file))

    bundleAssignment = generateBundleAssignmentWithDraft(valueationMatrix)

    solver = efxSolver.EFXSolver()

    if not isAllocEFX(bundleAssignment,valueationMatrix):

        (allocMatrix,donationlist,counter) = solver.findEFX(valueationMatrix,bundleAssignment)

        if counter > 0:
            print("**** NEW EXAMPLE ****")   
            print(valueationMatrix)
            print(bundleAssignment)
            print(allocMatrix)
            print(donationlist)
            print("counter : " + str(counter))
            print("*************")


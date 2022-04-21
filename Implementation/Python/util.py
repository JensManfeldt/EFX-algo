import numpy as np

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
            leastValuedItem = np.Infinity
            for k in range(agentsValueations.shape[1]):
                if alloc[j,k] > 0 and agentsValueations[i,k] < leastValuedItem:
                    leastValuedItem = agentsValueations[i,k]
            agentsEvalOfBundle = alloc[j,:] * agentsValueations[i,]
            if valueOfAssignedBundle < sum(agentsEvalOfBundle) - leastValuedItem:
                return False
    return True

def generateValueations(numAgents, numItems):
    valueMatrix = np.random.randint(1,10,[numAgents,numItems])
    return valueMatrix

def generateBundleAssignment(numAgents,numItems):
    bundleAssignement = np.zeros([numAgents,numItems], dtype=int)
    for k in range(numItems):
        bundleAssignement[np.random.randint(0,numAgents),k] = 1
    return bundleAssignement

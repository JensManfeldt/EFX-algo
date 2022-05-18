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
    valueMatrix = np.random.randint(1,1000,[numAgents,numItems])
    return valueMatrix

def generateBundleAssignment(numAgents,numItems):
    bundleAssignement = np.zeros([numAgents,numItems], dtype=int)
    for k in range(numItems):
        bundleAssignement[np.random.randint(0,numAgents),k] = 1
    return bundleAssignement

def generateBundleAssignmentWithDraftAndVariance(agentsValueations):
    copy = np.matrix.copy(agentsValueations)
    copy = (copy.T / np.mean(copy,axis=1)).T
    bundleAssignement = np.zeros([agentsValueations.shape[0],agentsValueations.shape[1]], dtype=int)
    agentsVariance = np.var(agentsValueations,axis=1, ddof=1)

    draftorder = []
    for i in range(len(agentsVariance)):
        draftorder.append(int(np.argmax(agentsVariance)))
        agentsVariance[draftorder[i]] = -1

    for j in range(agentsValueations.shape[1]):
        agentToPick = draftorder[j % agentsValueations.shape[0]]

        bestItem = int(np.argmax(copy[agentToPick,:]))
        
        bundleAssignement[agentToPick,bestItem] = 1

        copy[:,bestItem] = -1

    return bundleAssignement

def saveProblem(filename, agentsValueations,bundleAssignment):
    with open("/home/jens/Skrivebord/F2022/bachelor/EFX-algo/InterestingExamples/" + str(filename), "w+") as file: 
        file.write("Values\n")
        file.write(str(agentsValueations))
        file.write("\n")
        file.write("Assignment\n")
        file.write(str(bundleAssignment))

def generateRecursiveValues(numAgents, numItems):
    values = generateValueations(numAgents, numItems)
    bundleAssignment = generateBundleAssignmentWithDraft(values)

    temp = values[0,:] * bundleAssignment[0,:]
    mostValuedItem = int(np.argmax(temp))
    totalValue = sum(temp)

    values[0,mostValuedItem] = (totalValue-values[0,mostValuedItem]) - 1

    temp2 = values[1,:] * bundleAssignment[1,:]

    values[1,mostValuedItem] = sum(temp2) + 1

    return values

def checkConditions(agentsValueations, bundleAssignment):

    for i in range(agentsValueations.shape[0]):
        bundle = agentsValueations[i,:] * bundleAssignment[i,:]
        bundleValue = sum(bundle)
        for k in range(agentsValueations.shape[1]):
            if agentsValueations[i,k] > bundleValue:
                for j in range(agentsValueations.shape[0]):
                    if bundleAssignment[j,k] == 1:
                        otherAgentBundleValue = sum(agentsValueations[j,:] * bundleAssignment[j,:])
                        if 2*agentsValueations[j,k] < otherAgentBundleValue:
                            return True

    return False

def saveOptimalAlloction(filename, bundleAlloction, optNash):
    path = "/home/jens/Skrivebord/F2022/bachelor/EFX-algo/optimalNashAllocSpliddit/realData"
    with open(path + str(filename), "w+") as file:
        file.write(str(optNash) + "\n")
        for i in range(bundleAlloction.shape[0]):
            for j in range(bundleAlloction.shape[1]):
                file.write(str(bundleAlloction[i,j]) + "\n")
    




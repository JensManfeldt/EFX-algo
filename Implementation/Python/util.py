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
        file.write(agentsValueations)
        file.write("\n")
        file.write("Assignment\n")
        file.write(bundleAssignment)


values = np.array([[584, 422, 538, 594, 205, 288, 625, 487, 770],
                   [622, 478, 681, 909, 221, 874, 452, 527, 138],
                   [774, 137, 927, 147, 317, 313, 508,  15,  91],
                   [271, 182, 204, 326, 319, 354,  89, 435, 860]])

bundleAssignment = np.array([[0, 1, 0, 0, 0, 0, 1, 0, 1],
                             [0, 0, 0, 1, 0, 1, 0, 0, 0],
                             [1, 0, 1, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 1, 0, 0, 1, 0]])

saveProblem("test.txt", str(values), str(bundleAssignment))
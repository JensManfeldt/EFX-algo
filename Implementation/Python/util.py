import numpy as np
import scipy.optimize
import pandas as p
from math import floor
import matplotlib.pyplot as plt
import pathlib as path


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
        agentValueation = sum(agentsEvaluations[i,:] * bundleAssignment[i,:])
        
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

def generateBlindDraft(agentsValueations):
    
    bundleAssignement = np.zeros([agentsValueations.shape[0],agentsValueations.shape[1]], dtype=int)
    for j in range(agentsValueations.shape[1]):
        agentToGive = j % agentsValueations.shape[0]
        bundleAssignement[agentToGive, j] = 1
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

def generateBundleAssignmentRhoBound(agentsValueactions):

    copy = np.matrix.copy(agentsValueactions)

    # removeing zeros and make product to sum
    for i in range(copy.shape[0]):
        for j in range(copy.shape[1]):
            if copy[i,j] > 0:
                copy[i,j] = np.log(copy[i,j])
            else : 
                copy[i,j] = np.finfo(float).eps

    row,col = scipy.optimize.linear_sum_assignment(copy,maximize=True)
    
    copy = np.matrix.copy(agentsValueactions)
    
    bundleAssignment = np.zeros(agentsValueactions.shape)

    for i in range(len(row)):
        bundleAssignment[row[i],col[i]] = 1
        copy[:,col[i]] = -1
    
    for j in range(agentsValueactions.shape[1] - agentsValueactions.shape[0]):
        agentToPick = j % agentsValueactions.shape[0]

        bestItem = int(np.argmax(copy[agentToPick,:]))
        
        bundleAssignment[agentToPick,bestItem] = 1

        copy[:,bestItem] = -1

    return bundleAssignment

def rhoBoundWrong(agentsValueactions):

    copy = np.matrix.copy(agentsValueactions)

    row,col = scipy.optimize.linear_sum_assignment(copy,maximize=True)
    
    copy = np.matrix.copy(agentsValueactions)
    
    bundleAssignment = np.zeros(agentsValueactions.shape)

    for i in range(len(row)):
        bundleAssignment[row[i],col[i]] = 1
        copy[:,col[i]] = -1
    
    for j in range(agentsValueactions.shape[1] - agentsValueactions.shape[0]):
        agentToPick = j % agentsValueactions.shape[0]

        bestItem = int(np.argmax(copy[agentToPick,:]))
        
        bundleAssignment[agentToPick,bestItem] = 1

        copy[:,bestItem] = -1

    return bundleAssignment


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

def saveOptimalAlloction(filename, bundleAlloction, optNash, path):
    with open(path + str(filename), "w+") as file:
        file.write(str(optNash) + "\n")
        for i in range(bundleAlloction.shape[0]):
            for j in range(bundleAlloction.shape[1]):
                file.write(str(bundleAlloction[i,j]) + "\n")

def LoadoptimalExample(filename, numAgents, numItems, path):
    with open(path + "/" + filename,'r') as file: 
        text = file.read()
        lines = text.split('\n')
        optNash = lines[0]
        allocaMatrix = np.zeros([numAgents, numItems])
        for i in range(1,len(lines)-1):
            allocaMatrix[floor((i-1) / numItems), (i-1) % (numItems)] = int(lines[i][0])

    return allocaMatrix, float(optNash)

def writeToCSV(data, name):
    df = p.DataFrame(data)
    df.to_excel(name + ".xlsx",index=False)

def plotHeatMap(title,yaxisLables,xaxisLables, dataMatrix):
    
    fig, ax = plt.subplots()
    im = ax.imshow(dataMatrix,cmap="BuPu")

    ax.set_xticks(np.arange(len(xaxisLables)), labels=xaxisLables)
    ax.set_yticks(np.arange(len(yaxisLables)), labels=yaxisLables)
    plt.xticks(fontsize=6) 

    ax.set_title(title)
    fig.tight_layout()
    plt.savefig(str(title)+".png", dpi=200)

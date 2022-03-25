import unittest
import numpy as np
import efxSolver

class randomTester(unittest.TestCase):

    def test_test(self):
        solver = efxSolver.EFXSolver()
        
        numAgents = 0
        numItems = 0

        valueationMatrix = generateValueations(numAgents,numItems)
        bundleAssignment = generateBundleAssignment(numAgents, numItems)
        
        allocation, donationsList = solver.findEFX(valueationMatrix,bundleAssignment)
        print("Allocation")
        print(allocation)
        print("donationsList")
        return



def generateValueations(numAgents, numItems):
    valueMatrix = np.random.randint(1,100,[numAgents,numItems])
    return valueMatrix

def generateBundleAssignment(numAgents,numItems):
    bundleAssignement = np.zeros([numAgents,numItems], dtype=int)
    for k in range(numItems):
        bundleAssignement[np.random.randint(0,numAgents),k] = 1
    return bundleAssignement

def generateBundleAssignmentWithDraft(agentsValueations):
    copy = np.matrix.copy(agentsValueations)
    bundleAssignement = np.zeros([agentsValueations.shape[0],agentsValueations.shape[1]], dtype=int)
    for j in range(agentsValueations.shape[1]):
        agentToPick = j % agentsValueations.shape[0]

        bestItem = int(np.argmax(copy[agentToPick,:]))

        bundleAssignement[agentToPick,bestItem] = 1

        copy[:,bestItem] = 0

    return bundleAssignement



    
        

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



def calcNashWellFare(agentsEvaluations, bundleAssignment):
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


if __name__ == '__main__':
    np.random.seed(59)
    numAgents = 10
    numItems = 100
    for i in range(1000):
        valueationMatrix = generateValueations(numAgents,numItems)
        bundleAssignment = generateBundleAssignment(numAgents,numItems)
        nashBefore = calcNashWellFare(valueationMatrix,bundleAssignment)
        solver = efxSolver.EFXSolver()
        allocation, donationsList = solver.findEFX(valueationMatrix,bundleAssignment)
        nashAfter = calcNashWellFare(valueationMatrix,allocation)

        if not isAllocEFX(allocation,valueationMatrix) or  nashAfter < 1/2*nashBefore:
            print("Value Matrix")
            print(valueationMatrix)
            print("BundleAssignment")
            print(bundleAssignment)
            print("Allocation")
            print(allocation)
            print("donationsList")
            print(donationsList)
        else : 
            print("Example number : " + str(i) + " done")
            print("Nash Before : " + str(nashBefore) + " Nash After : " + str(nashAfter) + " The Ratio : " + str(100 * (nashAfter/nashBefore)))
        
    #unittest.main()
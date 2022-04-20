from operator import mod
import unittest
import numpy as np
import efxSolver
import pandas as pd

class randomTester(unittest.TestCase):

    def test_test(self):
        solver = efxSolver.EFXSolver()
        
        numAgents = 0
        numItems = 0

        valueationMatrix = generateValueations(numAgents,numItems)
        bundleAssignment = generateBundleAssignment(numAgents, numItems)
        
        allocation, donationsList = solver.algo1(valueationMatrix,bundleAssignment)
        print("Allocation")
        print(allocation)
        print("donationsList")
        return



def generateValueations(numAgents, numItems):
    valueMatrix = np.random.randint(1,10,[numAgents,numItems])
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

    for i in range(n):
        #print(bundleAssignment.shape)
        agentValueation = sum(agentsEvaluations[i,:] * bundleAssignment[i,:])
        #print("Agent : " + str(i) + " valueation is : " + str(agentValueation))
        
        agentValueation = pow(agentValueation,1/n)
        
        welFare *= agentValueation

    return welFare

def saveProblemAs(name,valueationMatrix,bundleAssignment):
    dataframe = pd.DataFrame(valueationMatrix)
    dataframe.to_csv(name + ".csv")
    
    #with open('valueationMatrix.txt', 'w') as file:
    #    for i in range(valueationMatrix.shape[0]):
    #        for j in range(valueationMatrix.shape[1]):
    #            padding = 3 - len(str(valueationMatrix[i,j]))
    #            print(padding)
    #            file.write(str(valueationMatrix[i,j]) + "|")
    #        file.write("\n")

if __name__ == '__main__':
    np.random.seed(2354)
    numAgents = 20
    numItems = 50
    for i in range(100000):
        valueationMatrix = generateValueations(numAgents,numItems)
        #bundleAssignment = generateBundleAssignment(numAgents,numItems)
        bundleAssignment = generateBundleAssignmentWithDraft(valueationMatrix)
        nashBefore = calcNashWellFare(valueationMatrix,bundleAssignment)
        #saveProblemAs("values",valueationMatrix,bundleAssignment)
        solver = efxSolver.EFXSolver()
        allocation, donationsList, counter = solver.findEFX(valueationMatrix,np.matrix.copy(bundleAssignment), 0)

        #print(isAllocEFX(np.matrix.copy(bundleAssignment),valueationMatrix))

        nashAfter = calcNashWellFare(valueationMatrix,allocation)

        if not isAllocEFX(allocation,valueationMatrix):
            print("Not efx")
            #print("Value Matrix")
            #print(valueationMatrix)
            #print("BundleAssignment")
            #print(bundleAssignment)
            #print("Allocation")
            #print(allocation)
            #print("donationsList")
            #print(donationsList)
            #print("Nash Before : " + str(nashBefore) + " Nash After : " + str(nashAfter) + " The Ratio : " + str(100 * (nashAfter/nashBefore)))
        elif nashAfter < 1/2*nashBefore:
            print("Nash below guarantee")
            print("Nash Before : " + str(nashBefore) + " Nash After : " + str(nashAfter) + " The Ratio : " + str(100 * (nashAfter/nashBefore)))
        #elif sum(donationsList) == 3:
        #    print("Value Matrix")
        #    print(valueationMatrix)
        #    print("BundleAssignment")
        #    print(bundleAssignment)
        #    print("Allocation")
        #    print(allocation)
        #    print("donationsList")
        #    print(donationsList)
        else : 
            print("Example number : " + str(i) + " done. After " + str(counter) + " recursive calls. Donated " + str(sum(donationsList)) + " items ")
            if(counter > 0):
                print("Value Matrix")
                print(valueationMatrix)
                print("BundleAssignment")
                print(bundleAssignment)
                print("Allocation")
                print(allocation)
                break
                #print("Nash Before : " + str(nashBefore) + " Nash After : " + str(nashAfter) + " The Ratio : " + str(100 * (nashAfter/nashBefore)))
    #unittest.main()
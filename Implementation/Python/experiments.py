from math import floor
import numpy as np
import efxSolver
import os
import adaptorSpliddit
import util as u
import pandas as p
## Does an agent envy the donated bundle



def runExperiment(agentsValueaction, problemName):
    n = valueationMatrix.shape[0]
    k = valueationMatrix.shape[1]
    solver = efxSolver.EFXSolver()

    recusiveUpperbound = pow(n,2) * k
    
    #Opt
    try :
        optAlloc, optimalNashBefore = LoadoptimalExample(problemName, n,k)
        optAlloc, optDonationList, optCounter = solver.findEFX(agentsValueaction,optAlloc,delta=0)
        optimalNashAfter = u.calcNashWellFare(agentsValueaction,optAlloc)
    except:
        optimalNashBefore = np.infty
        optimalNashAfter = np.infty

    #EF1
    EF1BundleAssignment = u.generateBundleAssignmentWithDraft(agentsValueaction)

    EF1NashBefore = u.calcNashWellFare(agentsValueaction,EF1BundleAssignment)

    if optimalNashBefore > 0:
        EF1rho = float(EF1NashBefore) / optimalNashBefore
    else:
        EF1rho = 1

    EF1Alloc, EF1donationList, EF1Counter = solver.findEFX(agentsValueaction, EF1BundleAssignment, delta=0)

    EF1envy, _ = envyOfDonatedItems(agentsValueaction,EF1Alloc,EF1donationList)

    EF1NashAfter = u.calcNashWellFare(agentsValueaction,EF1Alloc)

    #Matching
    MatchingBundleAssignment = u.generateBundleAssignmentRhoBound(agentsValueaction)

    MatchingNashBefore = u.calcNashWellFare(agentsValueaction,MatchingBundleAssignment)

    if optimalNashBefore > 0:
        Matchingrho = float(MatchingNashBefore) / optimalNashBefore
    else : 
        Matchingrho = 1

    MatchingAlloc, MatchingdonationList, MatchingCounter = solver.findEFX(agentsValueaction, MatchingBundleAssignment, delta=0)

    Matchingenvy, _ = envyOfDonatedItems(agentsValueaction,MatchingAlloc,MatchingdonationList)

    MatchingNashAfter = u.calcNashWellFare(agentsValueaction,MatchingAlloc)

    return [problemName, recusiveUpperbound, EF1Counter, MatchingCounter, optimalNashBefore, optimalNashAfter, EF1NashBefore, EF1NashAfter, EF1rho, EF1envy, MatchingNashBefore, MatchingNashAfter, Matchingrho, Matchingenvy] 


def LoadoptimalExample(filename, numAgents, numItems):
    with open("/home/jens/Skrivebord/F2022/bachelor/EFX-algo/optimalNashAllocSpliddit/realDatarealData"+filename,'r') as file: 
        text = file.read()
        lines = text.split('\n')
        optNash = lines[0]
        allocaMatrix = np.zeros([numAgents, numItems])
        for i in range(1,len(lines)-1):
            allocaMatrix[floor((i-1) / numItems), (i-1) % (numItems)] = int(lines[i][0])

    return allocaMatrix, float(optNash)

def envyOfDonatedItems(agentsValueaction, allocation, donationlist):

    bundleValueaction = agentsValueaction * allocation

    donatedValueactions = agentsValueaction * donationlist

    for i in range(bundleValueaction.shape[0]):
        valueaction = np.sum(bundleValueaction[i,:])
        leastValuedItem = np.infty
        for k in range(bundleValueaction.shape[1]):
            if donationlist[k] > 0 and donatedValueactions[i,k] < leastValuedItem:
                leastValuedItem = donatedValueactions[i,k]
        
        EFXdonated = np.sum(donatedValueactions[i,:]) - leastValuedItem
        if EFXdonated > valueaction:
            return True, i # i is the agent that envyes the donated set
    
    return False, -1 # no agent had envy

def writeToCSV(data):
    df = p.DataFrame(data)
    df.to_excel("data1.xlsx",index=False)

#def RecursiceUpperBound():



if __name__ == "__main__":
    dataPath = "/home/jens/Skrivebord/F2022/bachelor/EFX-algo/RealData/"
    allData = np.zeros([len(os.listdir(dataPath)),14])
    i = 0
    for file in os.listdir(dataPath):
        valueationMatrix = adaptorSpliddit.create_valueation_matrix(dataPath + str(file))
        #bundleAssign = u.generateBundleAssignmentWithDraft(valueationMatrix)

        #numAgents = np.random.randint(2,50)

        #numItems = np.random.randint(numAgents,numAgents*5)
        #valueationMatrix = u.generateRecursiveValues(numAgents,numItems)

        #print("Running experiment nr : " + str(file))
        data = runExperiment(valueationMatrix, file[8:])

            
        allData[i,:] = data
        i += 1
    
    writeToCSV(allData)
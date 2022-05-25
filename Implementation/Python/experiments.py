from uuid import UUID
import numpy as np
import efxSolver
import brute
import os
import adaptorSpliddit
import util as u
import warnings
## Does an agent envy the donated bundle


warnings.filterwarnings('ignore')

def runExperiment(agentsValueaction, problemName, optimalAlloc, optNashBefore):
    n = agentsValueaction.shape[0]
    k = agentsValueaction.shape[1]
    solver = efxSolver.EFXSolver()

    guaranteeOnNashWelfare = pow(2,1-1/n)
    recusiveUpperbound = pow(n,2) * k
    
    #Opt
    if np.sum(optimalAlloc) == 0:
        optimalNashBefore = np.infty
        optimalNashAfter = np.infty
        optimalrhoAfter = np.NaN
        optEnvy = 0
    else:
        optAlloc, optDonationList, _ = solver.findEFX(agentsValueaction,optimalAlloc,delta=0)
        optEnvy, _ = envyOfDonatedItems(agentsValueaction,optAlloc,optDonationList)
        optimalNashAfter = u.calcNashWellFare(agentsValueaction,optAlloc)
        optimalNashBefore = optNashBefore
        optimalrhoAfter = calculateRho(optimalNashBefore,optimalNashAfter)
        

    #EF1
    EF1BundleAssignment = u.generateBundleAssignmentWithDraft(agentsValueaction)

    EF1NashBefore = u.calcNashWellFare(agentsValueaction,EF1BundleAssignment)

    EF1rhoBefore = calculateRho(optimalNashBefore, EF1NashBefore)

    EF1Alloc, EF1donationList, EF1Counter = solver.findEFX(agentsValueaction, EF1BundleAssignment, delta=0)

    EF1envy, _ = envyOfDonatedItems(agentsValueaction,EF1Alloc,EF1donationList)

    EF1NashAfter = u.calcNashWellFare(agentsValueaction,EF1Alloc)

    EF1rhoAfter = calculateRho(optimalNashBefore,EF1NashAfter)

    #Matching
    MatchingBundleAssignment = u.generateBundleAssignmentRhoBound(agentsValueaction)

    MatchingNashBefore = u.calcNashWellFare(agentsValueaction,MatchingBundleAssignment)

    MatchingrhoBefore = calculateRho(optimalNashBefore,MatchingNashBefore)

    MatchingAlloc, MatchingdonationList, MatchingCounter = solver.findEFX(agentsValueaction, MatchingBundleAssignment, delta=0)

    Matchingenvy, _ = envyOfDonatedItems(agentsValueaction,MatchingAlloc,MatchingdonationList)

    MatchingNashAfter = u.calcNashWellFare(agentsValueaction,MatchingAlloc)

    MatchingrhoAfter = calculateRho(optimalNashBefore,MatchingNashAfter)

    return [problemName, recusiveUpperbound, EF1Counter, MatchingCounter, optimalNashBefore, optimalNashAfter, optEnvy, guaranteeOnNashWelfare, optimalrhoAfter, EF1NashBefore, EF1NashAfter, EF1rhoBefore, EF1rhoAfter, EF1envy, MatchingNashBefore, MatchingNashAfter, MatchingrhoBefore, MatchingrhoAfter, Matchingenvy] 

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

def ourAverage(list):
    divisor = 0
    accumulater = 0
    for i in range(len(list)):
        if list[i] != 0 and not np.isnan(list[i]) and not np.isinf(list[i]):
            divisor += 1
            accumulater += list[i]

    return 0 if divisor == 0 else accumulater / divisor

def ourAverage2(list):
    divisor = 0
    accumulater = 0
    for i in range(len(list)):
        if not np.isnan(list[i]) and not np.isinf(list[i]):
            divisor += 1
            accumulater += list[i]
    
    return 0 if divisor == 0 else accumulater / divisor

def calculateRho(optNash,compareNash):  
    if optNash > 0 and optNash != np.infty and compareNash > 0:
        return (float(compareNash) / optNash) * 100
    else : 
        if optNash == 0:
            return 1
        elif compareNash == 0:
            return 0
        else :
            return np.NaN

def calculateAggragateData(allData):
    optEnvy = sum(allData[:,6])
    EF1Envy = sum(allData[:,13])
    matchingEnvy = sum(allData[:,18])
    procentGuaranteeNashWith0 = ourAverage2((allData[:,4] - allData[:,5]) / (allData[:,4] / allData[:,7]) * 100)
    procentGuaranteeNash = ourAverage((allData[:,4] - allData[:,5]) / (allData[:,4] / allData[:,7]) * 100)
    optimalRhoAfter = ourAverage(allData[:,8])
    EF1rhoBefore = ourAverage(allData[:,11])
    EF1rhoAfter = ourAverage(allData[:,12])
    matchingrhoBefore = ourAverage(allData[:,16])
    matchingrhoAfter = ourAverage(allData[:,17])
    calcRepeatedRunsAvg = np.average(allData[:,1])
    EF1RepeatedRunsAvg = np.average(allData[:,2])
    matchingRepeatedRunsAvg = np.average(allData[:,3])
    EF1RepeatedRuns = sum(np.where(allData[:,2] > 0, 1, 0))
    matchingRepeatedRuns = sum(np.where(allData[:,3] > 0, 1, 0))

    print("Opt Envy : " + str(optEnvy))
    print("EF1 Envy : " + str(EF1Envy))
    print("Matching Envy : " + str(matchingEnvy))
    print("Average procent of Nash welfare guarantee : " + str(procentGuaranteeNashWith0))
    print("Average procent of Nash welfare guarantee when there is a donation : " + str(procentGuaranteeNash))
    print("Optimal average rho After : " + str(optimalRhoAfter))
    print("EF1 avarage RHO before :" + str(EF1rhoBefore))
    print("EF1 avarage RHO After :" + str(EF1rhoAfter))
    print("Mathcing avarage RHO before :" + str(matchingrhoBefore))
    print("Mathcing avarage RHO After :" + str(matchingrhoAfter))
    print("Calculated Average repeated runs : " + str(calcRepeatedRunsAvg))
    print("EF1 Average repeated runs : " + str(EF1RepeatedRunsAvg))
    print("Matching Average repeated runs : " + str(matchingRepeatedRunsAvg))
    print("EF1 Number of times repeated runs happens : " + str(EF1RepeatedRuns))
    print("Matching Number of times repeated runs happens : " + str(matchingRepeatedRuns))

    return  [optEnvy, EF1Envy, matchingEnvy, procentGuaranteeNashWith0, procentGuaranteeNash, optimalRhoAfter, EF1rhoBefore, EF1rhoAfter, matchingrhoBefore, matchingrhoAfter, calcRepeatedRunsAvg, EF1RepeatedRunsAvg, matchingRepeatedRunsAvg, EF1RepeatedRuns, matchingRepeatedRuns ]

def runFromData(dataPath, optDatapath, saveFileName):
    allData = np.zeros([len(os.listdir(dataPath)),19])
    i = 0
    for file in os.listdir(dataPath):
        valueationMatrix = adaptorSpliddit.create_valueation_matrix(dataPath + str(file))
        try :
            optimalAlloc, optimalNashBefore = u.LoadoptimalExample(file, valueationMatrix.shape[0],valueationMatrix.shape[1], optDatapath)
        except:
            optimalAlloc = np.zeros(valueationMatrix.shape)
            optimalNashBefore = np.inf

        data = runExperiment(valueationMatrix, file[8:], optimalAlloc, optimalNashBefore)
        allData[i,:] = data
        i += 1

    aggData = calculateAggragateData(allData)
    u.writeToCSV(allData, saveFileName)

    return allData, aggData

def runRandomExampleWithOptimalCalc(saveFileName, numRuns):
    allData = np.zeros([numRuns,19])
    for i in range(numRuns):
        numAgents = np.random.randint(2,5)
        numItems = np.random.randint(numAgents, numAgents+4)
        valueactionMatrix = u.generateValueations(numAgents, numItems)
        b = brute.Brute(numAgents, numItems, valueactionMatrix)
        optAlloc, optNash = b.findOptimalNash()
        allData[i,:] = runExperiment(valueactionMatrix,str(np.random.randint(i,(i+1)*10)), optAlloc,optNash)
    
    aggRandom = calculateAggragateData(allData)
    u.writeToCSV(allData,saveFileName)
    return allData, aggRandom

def runIntervalExperiment():
    ratioList = [1.2, 1.8, 2.2, 2.4, 2.6, 5]
    blindCounterAcc = np.zeros([len(ratioList)])
    EF1counterAcc = np.zeros([len(ratioList)])
    matchingCounterAcc = np.zeros([len(ratioList)])
    EF1Nash = np.zeros([len(ratioList)])
    matchingNash = np.zeros([len(ratioList)])

    runsPerIntervalPerAgent = 1000
    agentRange = 10

    solver = efxSolver.EFXSolver()
    for i in range(len(ratioList)):
        print("starting on ratio : " + str(ratioList[i]))
        for j in range(5,5+agentRange): 
            for _ in range(runsPerIntervalPerAgent):
                numAgents = j
                numItems = int(np.round(j * ratioList[i]))

                valueactionMatrix = u.generateValueations(numAgents, numItems)
                
                #blindAssignment = u.generateBlindDraft(valueactionMatrix)

                #_, _, blindCounter = solver.findEFX(valueactionMatrix,blindAssignment)

                EF1bundleAssignment = u.generateBundleAssignmentWithDraft(valueactionMatrix)
                EF1NashBefore = u.calcNashWellFare(valueactionMatrix, EF1bundleAssignment)
                EF1EFX, _, EF1counter = solver.findEFX(valueactionMatrix, EF1bundleAssignment)
                EF1NashAfter = u.calcNashWellFare(valueactionMatrix,EF1EFX)
                EF1Nash[i] += EF1NashAfter / EF1NashBefore

                matchingBundleAssignment = u.generateBundleAssignmentRhoBound(valueactionMatrix)
                matchingNashBefore = u.calcNashWellFare(valueactionMatrix, matchingBundleAssignment)
                matchingEFX, _, matchingCounter = solver.findEFX(valueactionMatrix, matchingBundleAssignment)
                matchingNashAfter = u.calcNashWellFare(valueactionMatrix, matchingEFX)
                matchingNash[i] += matchingNashAfter / matchingNashBefore

                #blindCounterAcc[i] += blindCounter
                EF1counterAcc[i] += EF1counter
                matchingCounterAcc[i] += matchingCounter
    
    runsPerInterval = agentRange * runsPerIntervalPerAgent
    #blindCounterAcc /= runsPerInterval
    EF1counterAcc /= runsPerInterval
    matchingCounterAcc /= runsPerInterval

    EF1Nash /= runsPerInterval
    matchingNash /= runsPerInterval
    #print("Blind Draft : " + str(blindCounterAcc))
    print("EF1 averages of repeated runs: " + str(EF1counterAcc))
    print("Matching averages of repeated runs: " + str(matchingCounterAcc))
    print("EF1 Procent of welfare retained on average: " + str(EF1Nash))
    print("Matching Procent of welfare retained on average: " + str(matchingNash))

    result = [ratioList, EF1counterAcc, matchingCounterAcc,EF1Nash, matchingNash]

    u.writeToCSV(result, "IntervalData")

if __name__ == "__main__":
    
    runIntervalExperiment()
    
    #aggData = np.zeros([3,15])
#
    #dataPath = "/home/jens/Skrivebord/F2022/bachelor/EFX-algo/RealData/"
    #optPath = "/home/jens/Skrivebord/F2022/bachelor/EFX-algo/optimalNashAllocSpliddit/realData"
    #realData, aggReal = runFromData(dataPath,optPath,"realData")
    #aggData[0,:] = aggReal
#
    #dataPath = "/home/jens/Skrivebord/F2022/bachelor/EFX-algo/DemoData/"
    #optPath = "/home/jens/Skrivebord/F2022/bachelor/EFX-algo/optimalNashDemo/"
    #demoData, aggDemo = runFromData(dataPath, optPath, "demoData")
    #aggData[1,:] = aggDemo
#
    #randomData, aggRandom = runRandomExampleWithOptimalCalc("randomExamples", 2000)
    #aggData[2,:] = aggRandom

    #u.writeToCSV(aggData, "AggData")

    
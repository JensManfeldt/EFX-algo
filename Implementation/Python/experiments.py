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

def runExperiment1():
    aggData = np.zeros([3,7])

    dataPath = "/home/jens/Skrivebord/F2022/bachelor/EFX-algo/RealData/"
    optPath = "/home/jens/Skrivebord/F2022/bachelor/EFX-algo/optimalNashAllocSpliddit/realData"
    realData, aggReal = runFromData(dataPath,optPath,"realData")
    aggData[0,:] = aggReal

    dataPath = "/home/jens/Skrivebord/F2022/bachelor/EFX-algo/DemoData/"
    optPath = "/home/jens/Skrivebord/F2022/bachelor/EFX-algo/optimalNashDemo/"
    demoData, aggDemo = runFromData(dataPath, optPath, "demoData")
    aggData[1,:] = aggDemo

    dataPath = "/home/jens/Skrivebord/F2022/bachelor/EFX-algo/randomExamples/"
    optPath = "/home/jens/Skrivebord/F2022/bachelor/EFX-algo/optimalRandom/"
    randomData, aggRandom = runFromData(dataPath, optPath, "randomData")
    aggData[2,:] = aggRandom

    aggergateDataWithDonationsExamples(realData, demoData, randomData)
    u.writeToCSV(aggData, "AggData")

def runRhoExperiment(agentsValueaction, problemName, optimalAlloc, optNashBefore):
    n = agentsValueaction.shape[0]
    k = agentsValueaction.shape[1]
    solver = efxSolver.EFXSolver()

    guaranteeOnNashWelfare = pow(2,1-1/n)
    
    
    #Opt
    if np.sum(optimalAlloc) == 0:
        optimalNashBefore = np.infty
        optimalNashAfter = np.infty
        optimalrhoAfter = np.NaN
        optEnvy = 0
        optDonationList = [0]
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

    EF1NashAfter = u.calcNashWellFare(agentsValueaction,EF1Alloc)

    EF1rhoAfter = calculateRho(optimalNashBefore,EF1NashAfter)

    #Matching
    MatchingBundleAssignment = u.generateBundleAssignmentRhoBound(agentsValueaction)

    MatchingNashBefore = u.calcNashWellFare(agentsValueaction,MatchingBundleAssignment)
    
    MatchingrhoBefore = calculateRho(optimalNashBefore,MatchingNashBefore)

    MatchingAlloc, MatchingdonationList, MatchingCounter = solver.findEFX(agentsValueaction, MatchingBundleAssignment, delta=0)

    MatchingNashAfter = u.calcNashWellFare(agentsValueaction,MatchingAlloc)

    MatchingrhoAfter = calculateRho(optimalNashBefore,MatchingNashAfter)

    return [int(problemName), optimalNashBefore, optimalNashAfter, guaranteeOnNashWelfare, optimalrhoAfter, EF1NashBefore, EF1NashAfter, EF1rhoBefore, EF1rhoAfter, MatchingNashBefore, MatchingNashAfter, MatchingrhoBefore, MatchingrhoAfter,np.sum(optDonationList), np.sum(EF1donationList),np.sum(MatchingdonationList)] 

def runSingleExperiment2(agentsValueaction, problemName, optPath):
    n = agentsValueaction.shape[0]
    k = agentsValueaction.shape[1]
    solver = efxSolver.EFXSolver()

    recusiveUpperbound = pow(n,2) * k
    try :
        optimalAssignment, optNash = u.LoadoptimalExample(problemName,n,k,optPath)
        optAlloc, optDonationList, _ = solver.findEFX(agentsValueaction,optimalAssignment)
        optEnvy, _ = envyOfDonatedItems(agentsValueaction, optAlloc, optDonationList)
    except:
        optEnvy = np.nan


    EF1BundleAssignment = u.generateBundleAssignmentWithDraft(agentsValueaction)

    EF1Alloc, EF1donationList, EF1Counter = solver.findEFX(agentsValueaction, EF1BundleAssignment, delta=0)

    EF1envy, _ = envyOfDonatedItems(agentsValueaction,EF1Alloc,EF1donationList)

    MatchingBundleAssignment = u.generateBundleAssignmentRhoBound(agentsValueaction)

    MatchingAlloc, MatchingdonationList, MatchingCounter = solver.findEFX(agentsValueaction, MatchingBundleAssignment, delta=0)

    Matchingenvy, _ = envyOfDonatedItems(agentsValueaction,MatchingAlloc,MatchingdonationList)

    return [int(problemName[8:]), recusiveUpperbound, EF1Counter, MatchingCounter, EF1envy, Matchingenvy, optEnvy]

def runExperiment2():
    pathRealData = "/home/jens/Skrivebord/F2022/bachelor/EFX-algo/RealData/" 
    pathDemoData = "/home/jens/Skrivebord/F2022/bachelor/EFX-algo/DemoData/"
    realDataMatrix = []
    demoDataMatrix = []
    realOptPath = "/home/jens/Skrivebord/F2022/bachelor/EFX-algo/optimalNashAllocSpliddit/realData"
    demoOptPath = "/home/jens/Skrivebord/F2022/bachelor/EFX-algo/optimalNashDemo/"
    for file in os.listdir(pathRealData):
        valueactionMatrix = adaptorSpliddit.create_valueation_matrix(pathRealData + str(file))
        data = runSingleExperiment2(valueactionMatrix,file, realOptPath)
        realDataMatrix.append(data)
    
    
    aggReal = calculateAggragateData2(np.array(realDataMatrix))
    

    for file in os.listdir(pathDemoData):
        valueactionMatrix = adaptorSpliddit.create_valueation_matrix(pathDemoData + str(file))
        data = runSingleExperiment2(valueactionMatrix,file, demoOptPath)
        demoDataMatrix.append(data)

    aggDemo = calculateAggragateData2(np.array(demoDataMatrix))

    aggData = [aggReal, aggDemo]

    u.writeToCSV(realDataMatrix, "experiment2RealData")
    u.writeToCSV(demoDataMatrix, "experiment2DemoData")
    u.writeToCSV(aggData, "experiment2Agg")

def runExperiment3and4():
    np.random.seed(12345678)
    ratioList = []
    ratioList = [x/10 for x in np.arange(10,41)]
    maxPossibleAgents = 20
    numIterations = 1000

    blindRetentionMatrix = np.zeros([maxPossibleAgents,len(ratioList)])
    EF1RetentionMatrix = np.zeros([maxPossibleAgents,len(ratioList)])
    matchingRentionMatrix = np.zeros([maxPossibleAgents,len(ratioList)])
    
    blindRetentionMatrix[0,:] = ratioList
    EF1RetentionMatrix[0,:] = ratioList
    matchingRentionMatrix[0,:] = ratioList

    blindEnvyMatrix = np.zeros([maxPossibleAgents,len(ratioList)])
    EF1EnvyMatrix = np.zeros([maxPossibleAgents,len(ratioList)])
    matchingEnvyMatrix = np.zeros([maxPossibleAgents,len(ratioList)])
    
    blindEnvyMatrix[0,:] = ratioList
    EF1EnvyMatrix[0,:] = ratioList
    matchingEnvyMatrix[0,:] = ratioList

    blindCounterMatrix = np.zeros([maxPossibleAgents,len(ratioList)])
    EF1CounterMatrix = np.zeros([maxPossibleAgents,len(ratioList)])
    matchingCounterMatrix = np.zeros([maxPossibleAgents,len(ratioList)])

    blindCounterMatrix[0,:] = ratioList
    EF1CounterMatrix[0,:] = ratioList
    matchingCounterMatrix[0,:] = ratioList


    solver = efxSolver.EFXSolver()

    for i in range(2,maxPossibleAgents+1):
        print("i is now : " + str(i))
        for j in range(len(ratioList)):
            for k in range(numIterations):
                valueationMatrix = u.generateValueations(i,int(np.floor(i*ratioList[j])))

                blindAssignment = u.generateBlindDraft(valueationMatrix)

                blindNashBefore = u.calcNashWellFare(valueationMatrix,blindAssignment)

                blindAlloc, blindDonationList, blindCounter = solver.findEFX(valueationMatrix, blindAssignment)

                blindEnvy, _ = envyOfDonatedItems(valueationMatrix, blindAlloc, blindDonationList)

                blindNashAfter = u.calcNashWellFare(valueationMatrix, blindAlloc)

                blindRetentionMatrix[i-1,j] += blindNashAfter / blindNashBefore

                if blindEnvy:
                    blindEnvyMatrix[i-1,j] += 1
                
                if blindCounter != 0:
                    blindCounterMatrix[i-1,j] += blindCounter

                EF1Assignment = u.generateBundleAssignmentWithDraft(valueationMatrix)

                EF1NashBefore = u.calcNashWellFare(valueationMatrix,EF1Assignment)

                EF1Alloc, EF1donationList, EF1counter = solver.findEFX(valueationMatrix, EF1Assignment)

                EF1Envy, _ = envyOfDonatedItems(valueationMatrix, EF1Alloc, EF1donationList)
                
                EF1NashAfter = u.calcNashWellFare(valueationMatrix, EF1Alloc)

                EF1RetentionMatrix[i-1,j] += EF1NashAfter / EF1NashBefore

                if EF1Envy:
                    EF1EnvyMatrix[i-1,j] += 1  
                
                if EF1counter != 0:
                    EF1CounterMatrix[i-1,j] += EF1counter

                matchingAssignment = u.generateBundleAssignmentRhoBound(valueationMatrix)

                matchingNashBefore = u.calcNashWellFare(valueationMatrix, matchingAssignment)

                matchingAlloc, matchingDonationList, matchingCounter = solver.findEFX(valueationMatrix, matchingAssignment)

                matchingEnvy, _ = envyOfDonatedItems(valueationMatrix, matchingAlloc, matchingDonationList)

                matchingNashAfter = u.calcNashWellFare(valueationMatrix, matchingAlloc)

                matchingRentionMatrix[i-1,j] += matchingNashAfter / matchingNashBefore

                if matchingEnvy:
                    matchingEnvyMatrix[i-1,j] += 1

                if matchingCounter != 0:
                    matchingCounterMatrix[i-1,j] += matchingCounter


                

    u.writeToCSV(blindEnvyMatrix,"experiment3blind")
    u.writeToCSV(EF1EnvyMatrix, "experiment3EF1")
    u.writeToCSV(matchingEnvyMatrix, "experiment3matching")

    blindCounterMatrix /= numIterations
    EF1CounterMatrix /= numIterations
    matchingCounterMatrix /= numIterations

    u.writeToCSV(blindCounterMatrix,"experiment4blind")
    u.writeToCSV(EF1CounterMatrix, "experiment4EF1")
    u.writeToCSV(matchingCounterMatrix ,"experiment4matching")

    blindEnvyMatrix = np.delete(blindEnvyMatrix,0,0)
    EF1EnvyMatrix = np.delete(EF1EnvyMatrix,0,0)
    matchingEnvyMatrix = np.delete(matchingEnvyMatrix,0,0)

    blindCounterMatrix = np.delete(blindCounterMatrix,0,0)
    EF1CounterMatrix = np.delete(EF1CounterMatrix,0,0)
    matchingCounterMatrix = np.delete(matchingCounterMatrix,0,0)

    u.plotHeatMap("experiment3blind",[x for x in range(2,maxPossibleAgents+1)], ratioList, blindEnvyMatrix)
    u.plotHeatMap("experiment3EF1",[x for x in range(2,maxPossibleAgents+1)], ratioList, EF1EnvyMatrix)
    u.plotHeatMap("experiment3matching",[x for x in range(2,maxPossibleAgents+1)], ratioList, matchingEnvyMatrix)

    u.plotHeatMap("experiment4blind",[x for x in range(2,maxPossibleAgents+1)], ratioList, blindCounterMatrix)
    u.plotHeatMap("experiment4EF1",[x for x in range(2,maxPossibleAgents+1)], ratioList, EF1CounterMatrix)
    u.plotHeatMap("experiment4matching",[x for x in range(2,maxPossibleAgents+1)], ratioList, matchingCounterMatrix)

    blindRetentionMatrix = (blindRetentionMatrix / numIterations) * 100
    EF1RetentionMatrix = (EF1RetentionMatrix / numIterations) * 100
    matchingRentionMatrix = (matchingRentionMatrix / numIterations) * 100

    u.writeToCSV(blindRetentionMatrix,"experiment5blind")
    u.writeToCSV(EF1RetentionMatrix, "experiment5EF1")
    u.writeToCSV(matchingRentionMatrix, "experiment5matching")

    blindRetentionMatrix = np.delete(blindRetentionMatrix,0,0)
    EF1RetentionMatrix = np.delete(EF1RetentionMatrix,0,0)
    matchingRentionMatrix = np.delete(matchingRentionMatrix,0,0)

    blindRetentionMatrix = 100 - blindRetentionMatrix
    EF1RetentionMatrix = 100 - EF1RetentionMatrix
    matchingRentionMatrix = 100 - matchingRentionMatrix

    u.plotHeatMap("experiment5blind",[x for x in range(2,maxPossibleAgents+1)], ratioList, blindRetentionMatrix)
    u.plotHeatMap("experiment5EF1",[x for x in range(2,maxPossibleAgents+1)], ratioList, EF1RetentionMatrix)
    u.plotHeatMap("experiment5matching",[x for x in range(2,maxPossibleAgents+1)], ratioList, matchingRentionMatrix)


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
            return 1, i # i is the agent that envyes the donated set
    
    return 0, -1 # no agent had envy

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

def calculateAggragateData1(allData):

    procentGuaranteeNashWith0 = ourAverage2((allData[:,1] - allData[:,2]) / (allData[:,1] / allData[:,3]) * 100)
    procentGuaranteeNash = ourAverage((allData[:,1] - allData[:,2]) / (allData[:,1] / allData[:,3]) * 100)
    optimalRhoAfter = ourAverage(allData[:,4])
    EF1rhoBefore = ourAverage(allData[:,7])
    EF1rhoAfter = ourAverage(allData[:,8])
    matchingrhoBefore = ourAverage(allData[:,11])
    matchingrhoAfter = ourAverage(allData[:,12])

    print("Average procent of Nash welfare guarantee : " + str(procentGuaranteeNashWith0))
    print("Average procent of Nash welfare guarantee when there is a donation : " + str(procentGuaranteeNash))
    print("Optimal average rho After : " + str(optimalRhoAfter))
    print("EF1 avarage RHO before :" + str(EF1rhoBefore))
    print("EF1 avarage RHO After :" + str(EF1rhoAfter))
    print("Mathcing avarage RHO before :" + str(matchingrhoBefore))
    print("Mathcing avarage RHO After :" + str(matchingrhoAfter))

    return  [procentGuaranteeNashWith0, procentGuaranteeNash, optimalRhoAfter, EF1rhoBefore, EF1rhoAfter, matchingrhoBefore, matchingrhoAfter ]

def ourSum(list):
    sum = 0
    for i in range(len(list)):
        if not np.isnan(list[i]):
            sum += list[i]
    return sum

def calculateAggragateData2(allData):
    optEnvy = ourSum(allData[:,6])
    EF1Envy = sum(allData[:,4])
    matchingEnvy = sum(allData[:,5])
    calcRepeatedRunsAvg = np.average(allData[:,1])
    EF1RepeatedRunsAvg = np.average(allData[:,2])
    matchingRepeatedRunsAvg = np.average(allData[:,3])
    EF1RepeatedRuns = sum(np.where(allData[:,2] > 0, 1, 0))
    matchingRepeatedRuns = sum(np.where(allData[:,3] > 0, 1, 0))

    print("optimal Envy : " + str(optEnvy))
    print("EF1 Envy : " + str(EF1Envy))
    print("Matching Envy : " + str(matchingEnvy))
    print("Calculated Average repeated runs : " + str(calcRepeatedRunsAvg))
    print("EF1 Average repeated runs : " + str(EF1RepeatedRunsAvg))
    print("Matching Average repeated runs : " + str(matchingRepeatedRunsAvg))
    print("EF1 Number of times repeated runs happens : " + str(EF1RepeatedRuns))
    print("Matching Number of times repeated runs happens : " + str(matchingRepeatedRuns))

    return [optEnvy, EF1Envy, matchingEnvy, calcRepeatedRunsAvg, EF1RepeatedRunsAvg, matchingRepeatedRunsAvg, EF1RepeatedRuns, matchingRepeatedRuns]

def runFromData(dataPath, optDatapath, saveFileName):
    allData = np.zeros([len(os.listdir(dataPath)),16])
    i = 0
    for file in os.listdir(dataPath):
        valueationMatrix = adaptorSpliddit.create_valueation_matrix(dataPath + str(file))
        try :
            optimalAlloc, optimalNashBefore = u.LoadoptimalExample(file, valueationMatrix.shape[0],valueationMatrix.shape[1], optDatapath)
        except:
            optimalAlloc = np.zeros(valueationMatrix.shape)
            optimalNashBefore = np.inf
        
        if len(file) > 13:
            data = runRhoExperiment(valueationMatrix, file[13:], optimalAlloc, optimalNashBefore)
        else:
            data = runRhoExperiment(valueationMatrix, file[8:], optimalAlloc, optimalNashBefore)
        
        allData[i,:] = data
        i += 1

    aggData = calculateAggragateData1(allData)
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
        allData[i,:] = runRhoExperiment(valueactionMatrix,str(np.random.randint(i,(i+1)*10)), optAlloc,optNash)
    
    aggRandom = calculateAggragateData1(allData)
    u.writeToCSV(allData,saveFileName)
    return allData, aggRandom

def aggergateDataWithDonationsExamples(realData, demoData, randomData):
    temp = [realData, demoData, randomData]
    aggData = []
    for d in range(len(temp)):
        data = temp[d]
        divsioers = [0,0,0]
        acc = [0,0,0,0,0]

        for i in range(data.shape[0]):
            if not np.isinf(data[i][1]): 
                if data[i][13] > 0:
                    divsioers[0] += 1
                    acc[0] += data[i][4]

                if data[i][14] > 0:
                    divsioers[1] += 1
                    acc[1] += data[i][7]
                    acc[2] += data[i][8]

                if data[i][15] > 0:
                    divsioers[2] += 1
                    acc[3] += data[i][11]
                    acc[4] += data[i][12]

        optNashAfter = acc[0] / divsioers[0]
        EF1NashBefore = acc[1] / divsioers[1]
        EF1NashAfter = acc[2] / divsioers[1]
        matchingNashBefore = acc[3] / divsioers[2]
        matchingNashAfter = acc[4] / divsioers[2]
        aggData.append([optNashAfter,EF1NashBefore,EF1NashAfter, matchingNashBefore, matchingNashAfter])
        
    u.writeToCSV(aggData,"aggWithdonations")


if __name__ == "__main__":

    #runExperiment1()

    runExperiment2()
    
    #runExperiment3and4()
    


    
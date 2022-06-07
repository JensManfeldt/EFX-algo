import numpy as np
import brute
import util as u
import pathlib as p

np.random.seed(12345678)

def makeAndSaveRandomProblem(numExamples):
    path = str(p.Path("../../randomExamples/randomExample").absolute().resolve())
    savePath = "/home/jens/Skrivebord/F2022/bachelor/EFX-algo/optimalRandom/"
    for i in range(numExamples):
        numAgents = np.random.randint(2,5)
        numItems = np.random.randint(numAgents, 12)
        print("running example " + str(i) + " with " + str(numAgents) + " agents and " + str(numItems) + " items")
        valueactionMatrix = u.generateValueations(numAgents, numItems)

        with open(path + str(i),"w+") as file:
            for j in range(valueactionMatrix.shape[0]):
                for k in range(valueactionMatrix.shape[1]):
                    first = j
                    second = k
                    third = valueactionMatrix[j,k]
                    file.write(str(first) + ", " + str(second) + ", " + str(int(third)) + "\n")

        b = brute.Brute(numAgents, numItems, valueactionMatrix)
        optAlloc, optNash = b.findOptimalNash()

        u.saveOptimalAlloction("randomExample" + str(i), optAlloc, optNash, savePath)

makeAndSaveRandomProblem(10000)
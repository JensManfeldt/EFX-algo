import numpy as np
import efxSolver
import util as u    

if __name__ == '__main__':
    np.random.seed(112345)

    for i in range(500000):
        if i % 100 == 0:
            print(i) 
        numAgents = np.random.randint(2,50)

        numItems = np.random.randint(numAgents,numAgents*5+1)
        valueationMatrix = u.generateValueations(numAgents,numItems)

        bundleAssignment = u.generateBlindDraft(valueationMatrix)

        nashBefore = u.calcNashWellFare(valueationMatrix,bundleAssignment)
        
        solver = efxSolver.EFXSolver()

        allocation, donationsList, counter = solver.multipleRuns(valueationMatrix,np.matrix.copy(bundleAssignment), 0)

        nashAfter = u.calcNashWellFare(valueationMatrix,allocation)
        if not u.isAllocEFX(allocation,valueationMatrix): # the algo have made a mistake
            print("Not efx")
            print("Value Matrix")
            print(valueationMatrix)
            print("BundleAssignment")
            print(bundleAssignment)
            print("Allocation")
            print(allocation)
            print("donationsList")
            print(donationsList)
            print("Nash Before : " + str(nashBefore) + " Nash After : " + str(nashAfter) + " The Ratio : " + str(100 * (nashAfter/nashBefore)))
            u.saveProblem(str(i) + "EFX Bug",valueationMatrix,bundleAssignment)
            break
        elif nashAfter < 1/2*nashBefore: # Algo made a mistake
            print("Nash below guarantee")
            print("Value Matrix")
            print(valueationMatrix)
            print("BundleAssignment")
            print(bundleAssignment)
            print("Allocation")
            print(allocation)
            print("donationsList")
            print(donationsList)
            print("Nash Before : " + str(nashBefore) + " Nash After : " + str(nashAfter) + " The Ratio : " + str(100 * (nashAfter/nashBefore)))
            u.saveProblem(str(i) + "Nash Bug",valueationMatrix,bundleAssignment)
            break
        
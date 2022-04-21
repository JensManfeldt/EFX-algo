import numpy as np
import efxSolver
import util as u    

if __name__ == '__main__':
    np.random.seed(2354)
    numAgents = 3
    numItems = 5
    for i in range(100000):
        valueationMatrix = u.generateValueations(numAgents,numItems)

        bundleAssignment = u.generateBundleAssignmentWithDraft(valueationMatrix)

        nashBefore = u.calcNashWellFare(valueationMatrix,bundleAssignment)
        
        solver = efxSolver.EFXSolver()

        allocation, donationsList, counter = solver.findEFX(valueationMatrix,np.matrix.copy(bundleAssignment), 0)

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
            break
        else : 
            print("Example number : " + str(i) + " done. After " + str(counter) + " recursive calls. Donated " + str(sum(donationsList)) + " items ")


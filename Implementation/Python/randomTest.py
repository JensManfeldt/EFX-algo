import numpy as np
import efxSolver
import util as u    

if __name__ == '__main__':
    np.random.seed(420)

    for i in range(100000):
        numAgents = np.random.randint(2,101)

        numItems = np.random.randint(1,np.random.randint(1,5)*numAgents+1)+numAgents
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
            u.saveProblem(i,valueationMatrix,bundleAssignment)
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
            u.saveProblem(i,valueationMatrix,bundleAssignment)
        elif counter > 0:
            print("**** NEW EXAMPLE **** ")
            print("Value Matrix")
            print(valueationMatrix)
            print("BundleAssignment")
            print(bundleAssignment)
            print("Allocation")
            print(allocation)
            print("donationsList")
            print(donationsList)
            print("************")
            u.saveProblem(i,valueationMatrix,bundleAssignment)

        else : 
            print("Example number : " + str(i) + " with " + str(numAgents) + " agents and " + str(numItems) + " items done. After " + str(counter) + " recursive calls. Donated " + str(sum(donationsList)) + " items ")
            


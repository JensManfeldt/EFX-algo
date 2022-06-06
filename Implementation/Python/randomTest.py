import numpy as np
import efxSolver
import util as u    

if __name__ == '__main__':
    np.random.seed(112345)

    for i in range(500000):
        if i % 1000 == 0:
            print(i)
        numAgents = np.random.randint(2,50)

        numItems = np.random.randint(numAgents,numAgents*5+1)
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
        #elif counter > 0:
        #    print("**** NEW EXAMPLE **** ")
        #    print("Value Matrix")
        #    print(valueationMatrix)
        #    print("BundleAssignment")
        #    print(bundleAssignment)
        #    print("Allocation")
        #    print(allocation)
        #    print("donationsList")
        #    print(donationsList)
        #    print("************")
        #    u.saveProblem(str(i) + "VarianceExample" ,valueationMatrix,bundleAssignment)
        #    break

        #else : 
        #    print("Example number : " + str(i) + " with " + str(numAgents) + " agents and " + str(numItems) + " items done. After " + str(counter) + " recursive calls. Donated " + str(sum(donationsList)) + " items ")
            


import adaptorSpliddit
import efxSolver
import os
import util as u

realdataPath = "/home/jens/Skrivebord/F2022/bachelor/EFX-algo/RealData/"

demoDataPath = "/home/jens/Skrivebord/F2022/bachelor/EFX-algo/DemoData/"

dataPath = "/home/jens/Skrivebord/F2022/bachelor/EFX-algo/InterestingExamples/"

def testAll():
    for file in os.listdir(dataPath):
        valueationMatrix = adaptorSpliddit.create_valueation_matrix(dataPath + str(file))

        bundleAssignment = u.generateBundleAssignmentWithDraftAndVariance(valueationMatrix)

        solver = efxSolver.EFXSolver()

        if not u.isAllocEFX(bundleAssignment,valueationMatrix):

            (allocMatrix,donationlist,counter) = solver.findEFX(valueationMatrix,bundleAssignment)

            if counter > 0:
                print("**** NEW EXAMPLE ****")   
                print(valueationMatrix)
                print(bundleAssignment)
                print(allocMatrix)
                print(donationlist)
                print("counter : " + str(counter))
                print("*************")



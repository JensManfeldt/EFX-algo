import unittest
import numpy as np
import util as u

import efxSolver


class Test(unittest.TestCase):

    def test_VerySimpleBasic(self):
        bundleAssignemnts = np.array([[1,0],
                                      [0,1]])
        agentValueations = np.array([[3,2],
                                     [2,3]])

        solver = efxSolver.EFXSolver()
        matching, donationList = solver.basicAlgorithm(agentValueations,bundleAssignemnts)
        np.testing.assert_array_equal(matching,np.array([[1,0],[0,1]]))
        np.testing.assert_array_equal(donationList,np.array([0,0]))

    def test_VerySimpleAdvanced(self):
        bundleAssignemnts = np.array([[1,0],
                                      [0,1]])
        agentValueations = np.array([[3,2],
                                     [2,3]])

        solver = efxSolver.EFXSolver()
        matching, donationList, efx = solver.advancedAlgorithm(agentValueations,bundleAssignemnts,0.5)
        np.testing.assert_array_equal(matching,np.array([[1,0],[0,1]]))
        np.testing.assert_array_equal(donationList,np.array([0,0]))
        self.assertTrue(efx)
    
    def test_BadAssignmentSimpleBasic(self):
        bundleAssignemnts = np.array([[0,1],
                                      [1,0]])
        agentValueations = np.array([[3,2],
                                     [2,3]])

        solver = efxSolver.EFXSolver()
        matching, donationList = solver.basicAlgorithm(agentValueations,bundleAssignemnts)
        np.testing.assert_array_equal(matching,np.array([[0,1],
                                                         [1,0]]))
        np.testing.assert_array_equal(donationList,np.array([0,0]))

    def test_BadAssignmentSimpleAdvanced(self):
        bundleAssignemnts = np.array([[0,1],
                                      [1,0]])
        agentValueations = np.array([[3,2],
                                     [2,3]])

        solver = efxSolver.EFXSolver()
        matching, donationList, efx = solver.advancedAlgorithm(agentValueations,bundleAssignemnts,0.5)
        np.testing.assert_array_equal(matching,np.array([[0,1],
                                                         [1,0]]))
        np.testing.assert_array_equal(donationList,np.array([0,0]))
        self.assertTrue(efx)

    def test_DonationWorksBasic(self):
        agentValueations = np.array([[1, 5, 4, 3, 7],
                                     [3, 7, 4, 4, 1], 
                                     [8, 8, 1, 3, 6], 
                                     [2, 1, 9, 2, 3]])

        bundleAssignemnts = np.array([[0, 0, 0, 0, 1],
                                      [0, 1, 1, 0, 0],
                                      [1, 0, 0, 0, 0], 
                                      [0, 0, 0, 1, 0]])

        solver = efxSolver.EFXSolver()
        matching, donationList = solver.basicAlgorithm(agentValueations,bundleAssignemnts)
        
        np.testing.assert_array_equal(matching,np.array([[0,0,0,0,1],
                                                         [0,0,1,0,0],
                                                         [1,0,0,0,0],
                                                         [0,0,0,1,0]]))
        np.testing.assert_array_equal(donationList,np.array([0,1,0,0,0]))

    def test_DonationWorksAdvanced(self):
        agentValueations = np.array([[1, 5, 4, 3, 7],
                                     [3, 7, 4, 4, 1], 
                                     [8, 8, 1, 3, 6], 
                                     [2, 1, 9, 2, 3]])

        bundleAssignemnts = np.array([[0, 0, 0, 0, 1],
                                      [0, 1, 1, 0, 0],
                                      [1, 0, 0, 0, 0], 
                                      [0, 0, 0, 1, 0]])

        solver = efxSolver.EFXSolver()
        matching, donationList, efx = solver.advancedAlgorithm(agentValueations,bundleAssignemnts,0)
        
        np.testing.assert_array_equal(matching,np.array([[0,0,0,0,1],
                                                         [0,1,0,0,0],
                                                         [1,0,0,0,0],
                                                         [0,0,1,1,0]]))
        np.testing.assert_array_equal(donationList,np.array([0,0,0,0,0]))
        self.assertFalse(efx)

    def test_DonationWorksRecursive(self):
        agentValueations = np.array([[1, 5, 4, 3, 7],
                                     [3, 7, 4, 4, 1], 
                                     [8, 8, 1, 3, 6], 
                                     [2, 1, 9, 2, 3]])

        bundleAssignemnts = np.array([[0, 0, 0, 0, 1],
                                      [0, 1, 1, 0, 0],
                                      [1, 0, 0, 0, 0], 
                                      [0, 0, 0, 1, 0]])

        solver = efxSolver.EFXSolver()
        matching, donationList, counter = solver.multipleRuns(agentValueations,bundleAssignemnts)
        
        np.testing.assert_array_equal(matching,np.array([[0,0,0,0,1],
                                                         [0,1,0,0,0],
                                                         [1,0,0,0,0],
                                                         [0,0,1,1,0]]))
        np.testing.assert_array_equal(donationList,np.array([0,0,0,0,0]))
        self.assertEqual(counter,1)
        

    def test_AssignmentWithAnAgentNotGettingOrginalBundleBasic(self):
        agentValueations = np.array([[1, 5, 4, 3, 7, 2],
                                     [3, 7, 4, 4, 1, 8], 
                                     [8, 8, 1, 3, 6, 2], 
                                     [2, 1, 9, 2, 3, 3]])

        bundleAssignemnts = np.array([[0, 0, 0, 0, 1, 0],
                                      [0, 1, 1, 0, 0, 0],
                                      [1, 0, 0, 0, 0, 0], 
                                      [0, 0, 0, 1, 0, 1]])

        solver = efxSolver.EFXSolver()
        matching, donationList = solver.basicAlgorithm(agentValueations,bundleAssignemnts)
        
        np.testing.assert_array_equal(matching,np.array([[0,0,0,0,1,0],
                                                         [0,0,0,1,0,1],
                                                         [1,0,0,0,0,0],
                                                         [0,0,1,0,0,0]]))
        np.testing.assert_array_equal(donationList,np.array([0,1,0,0,0,0]))
    

    def test_AssignmentWithAnAgentNotGettingOrginalBundleAdvanced(self):
        agentValueations = np.array([[1, 5, 4, 3, 7, 2],
                                     [3, 7, 4, 4, 1, 8], 
                                     [8, 8, 1, 3, 6, 2], 
                                     [2, 1, 9, 2, 3, 3]])

        bundleAssignemnts = np.array([[0, 0, 0, 0, 1, 0],
                                      [0, 1, 1, 0, 0, 0],
                                      [1, 0, 0, 0, 0, 0], 
                                      [0, 0, 0, 1, 0, 1]])

        solver = efxSolver.EFXSolver()
        matching, donationList, efx = solver.advancedAlgorithm(agentValueations,bundleAssignemnts,0)
        
        np.testing.assert_array_equal(matching,np.array([[0,0,0,0,1,0],
                                                         [0,1,0,0,0,0],
                                                         [1,0,0,0,0,0],
                                                         [0,0,1,1,0,1]]))
        np.testing.assert_array_equal(donationList,np.array([0,0,0,0,0,0]))
        self.assertFalse(efx)

    def test_AssignmentWithAnAgentNotGettingOrginalBundleRecursive(self):
        agentValueations = np.array([[1, 5, 4, 3, 7, 2],
                                     [3, 7, 4, 4, 1, 8], 
                                     [8, 8, 1, 3, 6, 2], 
                                     [2, 1, 9, 2, 3, 3]])

        bundleAssignemnts = np.array([[0, 0, 0, 0, 1, 0],
                                      [0, 1, 1, 0, 0, 0],
                                      [1, 0, 0, 0, 0, 0], 
                                      [0, 0, 0, 1, 0, 1]])

        solver = efxSolver.EFXSolver()
        matching, donationList, counter = solver.multipleRuns(agentValueations,bundleAssignemnts)
        
        np.testing.assert_array_equal(matching,np.array([[0,0,0,0,1,0],
                                                         [0,1,0,1,0,0],
                                                         [1,0,0,0,0,0],
                                                         [0,0,1,0,0,0]]))
        np.testing.assert_array_equal(donationList,np.array([0,0,0,0,0,1]))
        self.assertEqual(counter,2)

    def test_CaseWithTwoDonationsBasic(self):
        agentValueations = np.array([[3, 2, 1, 1, 1],
                                     [3, 2, 1, 1, 1], 
                                     [3, 2, 1, 1, 1]])

        bundleAssignemnts = np.array([[1, 1, 1, 0, 0],
                                      [0, 0, 0, 1, 0],
                                      [0, 0, 0, 0, 1]])

        solver = efxSolver.EFXSolver()
        matching, donationList = solver.basicAlgorithm(agentValueations,bundleAssignemnts)

        np.testing.assert_array_equal(matching,np.array([[1, 0, 0, 0, 0],
                                                         [0, 0, 0, 1, 0],
                                                         [0, 0, 0, 0, 1]]))
        np.testing.assert_array_equal(donationList,np.array([0,1,1,0,0]))

    def test_CaseWithTwoDonationsAdvanced(self):
        agentValueations = np.array([[3, 2, 1, 1, 1],
                                     [3, 2, 1, 1, 1], 
                                     [3, 2, 1, 1, 1]])

        bundleAssignemnts = np.array([[1, 1, 1, 0, 0],
                                      [0, 0, 0, 1, 0],
                                      [0, 0, 0, 0, 1]])

        solver = efxSolver.EFXSolver()
        matching, donationList, efx = solver.advancedAlgorithm(agentValueations,bundleAssignemnts,0)

        np.testing.assert_array_equal(matching,np.array([[1, 0, 0, 0, 0],
                                                         [0, 0, 0, 1, 0],
                                                         [0, 0, 0, 0, 1]]))
        np.testing.assert_array_equal(donationList,np.array([0,1,1,0,0]))
        self.assertTrue(efx) 
    
    def test_OneAgentHasAllItemsBasic(self):
        agentValueations = np.array([[3, 2, 1, 1, 1],
                                     [3, 2, 1, 1, 1], 
                                     [3, 2, 1, 1, 1]])

        bundleAssignemnts = np.array([[1, 1, 1, 1, 1],
                                      [0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0]])

        solver = efxSolver.EFXSolver()
        matching, donationList = solver.basicAlgorithm(agentValueations,bundleAssignemnts)

        np.testing.assert_array_equal(matching,np.array([[1, 0, 0, 0, 0],
                                                         [0, 0, 0, 0, 0],
                                                         [0, 0, 0, 0, 0]]))
        np.testing.assert_array_equal(donationList,np.array([0,1,1,1,1]))
    
    def test_OneAgentHasAllItemsAdvanced(self):
        agentValueations = np.array([[3, 2, 1, 1, 1],
                                     [3, 2, 1, 1, 1], 
                                     [3, 2, 1, 1, 1]])

        bundleAssignemnts = np.array([[1, 1, 1, 1, 1],
                                      [0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0]])

        solver = efxSolver.EFXSolver()
        matching, donationList, efx = solver.advancedAlgorithm(agentValueations,bundleAssignemnts,0)

        np.testing.assert_array_equal(matching,np.array([[0, 1, 1, 1, 1],
                                                         [1, 0, 0, 0, 0],
                                                         [0, 0, 0, 0, 0]]))
        np.testing.assert_array_equal(donationList,np.array([0,0,0,0,0]))
        self.assertFalse(efx)
    
    def test_OneAgentHasAllItemsRecurive(self):
        agentValueations = np.array([[3, 2, 1, 1, 1],
                                     [3, 2, 1, 1, 1], 
                                     [3, 2, 1, 1, 1]])

        bundleAssignemnts = np.array([[1, 1, 1, 1, 1],
                                      [0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0]])

        solver = efxSolver.EFXSolver()
        matching, donationList, counter = solver.multipleRuns(agentValueations,bundleAssignemnts)

        np.testing.assert_array_equal(matching,np.array([[0, 0, 1, 1, 1],
                                                         [1, 0, 0, 0, 0],
                                                         [0, 1, 0, 0, 0]]))
        np.testing.assert_array_equal(donationList,np.array([0,0,0,0,0]))
        self.assertEqual(counter,2)

    
    def test_updateXPathLen0(self):
        agentValueations = np.array([[3, 2, 1, 1, 1],
                                     [3, 2, 1, 1, 1], 
                                     [3, 2, 1, 1, 1]])

        bundleAssignemnts = np.array([[1, 1, 1, 1, 1],
                                      [0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0]])

        solver = efxSolver.EFXSolver()
        solver.setUp(agentValueations,bundleAssignemnts)

        solver.bundleAssignmentZ = np.array([[1, 1, 0, 1, 1],
                                            [0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0]])
        path = np.array([])
        robustDemandBundle = 0
        unmatchedAgent = 1

        solver.updateOrginalAlloc(path,robustDemandBundle,unmatchedAgent)

        np.testing.assert_array_equal(solver.bundleAssignmentX,np.array([[0, 0, 1, 0, 0],
                                                                         [1, 1, 0, 1, 1],
                                                                         [0, 0, 0, 0, 0]]) )

    def test_updateXPathLen1(self):
        agentValueations = np.array([[3, 2, 1, 1, 1],
                                     [3, 2, 1, 1, 1], 
                                     [3, 2, 5, 5, 1]])

        bundleAssignemnts = np.array([[1, 1, 0, 0, 0],
                                      [0, 0, 1, 1, 0],
                                      [0, 0, 0, 0, 1]])

        solver = efxSolver.EFXSolver()
        solver.setUp(agentValueations,bundleAssignemnts)

        solver.bundleAssignmentZ = np.array([[1, 0, 0, 0, 0],
                                            [0, 0, 1, 1, 0],
                                            [0, 0, 0, 0, 1]])
        path = np.array([[2,1]])
        robustDemandBundle = 0
        unmatchedAgent = 1

        solver.updateOrginalAlloc(path,robustDemandBundle,unmatchedAgent)

        np.testing.assert_array_equal(solver.bundleAssignmentX,np.array([[0, 1, 0, 0, 0],
                                                                         [1, 0, 0, 0, 0],
                                                                         [0, 0, 1, 1, 1]]) )

    def test_updateXPathLen4(self):
        agentValueations = np.array([[1, 3, 2, 1, 1, 1 ],
                                     [1, 10, 2, 1, 1, 1], 
                                     [1, 3, 10, 5, 5, 1],
                                     [1, 1, 1, 10, 1, 1],
                                     [1, 1, 1, 1, 10, 1],
                                     [1, 1, 1, 1, 1, 10]])

        bundleAssignemnts = np.array([[1, 1, 0, 0, 0, 0],
                                      [0, 0, 1, 0, 0, 0],
                                      [0, 0, 0, 1, 0, 0],
                                      [0, 0, 0, 0, 1, 0],
                                      [0, 0, 0, 0, 0, 1],
                                      [0, 0, 0, 0, 0, 0]])

        solver = efxSolver.EFXSolver()
        solver.setUp(agentValueations,bundleAssignemnts)

        solver.bundleAssignmentZ = np.array([[0, 1, 0, 0, 0, 0],
                                            [0, 0, 1, 0, 0, 0],
                                            [0, 0, 0, 1, 0, 0],
                                            [0, 0, 0, 0, 1, 0],
                                            [0, 0, 0, 0, 0, 1],
                                            [0, 0, 0, 0, 0, 0]])

        path = np.array([[5,4],[4,3],[3,2],[2,1]])
        robustDemandBundle = 0
        unmatchedAgent = 1

        solver.updateOrginalAlloc(path,robustDemandBundle,unmatchedAgent)

        np.testing.assert_array_equal(solver.bundleAssignmentX,np.array([[1, 0, 0, 0, 0, 0],
                                                                         [0, 1, 0, 0, 0, 0],
                                                                         [0, 0, 1, 0, 0, 0],
                                                                         [0, 0, 0, 1, 0, 0],
                                                                         [0, 0, 0, 0, 1, 0],
                                                                         [0, 0, 0, 0, 0, 1]]))

    def test_followPathLen4(self):
        agentValueations = np.array([[1, 3, 2, 1, 1, 1 ],
                                     [1, 10, 2, 1, 1, 1], 
                                     [1, 3, 10, 5, 5, 1],
                                     [1, 1, 1, 10, 1, 1],
                                     [1, 1, 1, 1, 10, 1],
                                     [1, 1, 1, 1, 1, 10]])

        bundleAssignemnts = np.array([[1, 1, 0, 0, 0, 0],
                                      [0, 0, 1, 0, 0, 0],
                                      [0, 0, 0, 1, 0, 0],
                                      [0, 0, 0, 0, 1, 0],
                                      [0, 0, 0, 0, 0, 1],
                                      [0, 0, 0, 0, 0, 0]])

        solver = efxSolver.EFXSolver()
        solver.setUp(agentValueations,bundleAssignemnts)

        matching = np.array([[5,4],[4,3],[3,2],[2,1],[0,0]])

        path, _ = solver.followPath(5,matching)

        np.testing.assert_array_equal(path, np.array([[5,4],[4,3],[3,2],[2,1]]))

    def test_followPathNoPath(self):
        agentValueations = np.array([[3, 2, 1, 1, 1],
                                     [3, 2, 1, 1, 1], 
                                     [3, 2, 1, 1, 1]])

        bundleAssignemnts = np.array([[1, 1, 1, 1, 1],
                                      [0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0]])

        solver = efxSolver.EFXSolver()
        solver.setUp(agentValueations,bundleAssignemnts)       

        matching = np.array([[0,0]])

        path, _ = solver.followPath(1,matching)

        np.testing.assert_array_equal(path,[])




if __name__ == '__main__':
    unittest.main()
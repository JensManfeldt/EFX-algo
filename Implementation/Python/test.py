import unittest
import numpy as np

import efxSolver



class Test(unittest.TestCase):

    def test_VerySimple(self):
        bundleAssignemnts = np.array([[1,0],
                                      [0,1]])
        agentValueations = np.array([[3,2],
                                     [2,3]])

        solver = efxSolver.EFXSolver(agentValueations,bundleAssignemnts)
        matching, donationList = solver.findEFX()
        np.testing.assert_array_equal(matching,np.array([[1,0],[0,1]]))
        np.testing.assert_array_equal(donationList,np.array([0,0]))

    def test_BadAssignmentSimple(self):
        bundleAssignemnts = np.array([[0,1],
                                      [1,0]])
        agentValueations = np.array([[3,2],
                                     [2,3]])

        solver = efxSolver.EFXSolver(agentValueations,bundleAssignemnts)
        matching, donationList = solver.findEFX()
        np.testing.assert_array_equal(matching,np.array([[0,1],
                                                         [1,0]]))
        np.testing.assert_array_equal(donationList,np.array([0,0]))

    def test_DonationWorks(self):
        agentValueations = np.array([[1, 5, 4, 3, 7],
                                     [3, 7, 4, 4, 1], 
                                     [8, 8, 1, 3, 6], 
                                     [2, 1, 9, 2, 3]])

        bundleAssignemnts = np.array([[0, 0, 0, 0, 1],
                                      [0, 1, 1, 0, 0],
                                      [1, 0, 0, 0, 0], 
                                      [0, 0, 0, 1, 0]])

        solver = efxSolver.EFXSolver(agentValueations,bundleAssignemnts)
        matching, donationList = solver.findEFX()
        
        np.testing.assert_array_equal(matching,np.array([[0,0,0,0,1],
                                                         [0,0,1,0,0],
                                                         [1,0,0,0,0],
                                                         [0,0,0,1,0]]))
        np.testing.assert_array_equal(donationList,np.array([0,1,0,0,0]))

    def test_AssignmentWithAnAgentNotGettingOrginalBundle(self):
        agentValueations = np.array([[1, 5, 4, 3, 7, 2],
                                     [3, 7, 4, 4, 1, 8], 
                                     [8, 8, 1, 3, 6, 2], 
                                     [2, 1, 9, 2, 3, 3]])

        bundleAssignemnts = np.array([[0, 0, 0, 0, 1, 0],
                                      [0, 1, 1, 0, 0, 0],
                                      [1, 0, 0, 0, 0, 0], 
                                      [0, 0, 0, 1, 0, 1]])

        solver = efxSolver.EFXSolver(agentValueations,bundleAssignemnts)
        matching, donationList = solver.findEFX()
        
        np.testing.assert_array_equal(matching,np.array([[0,0,0,0,1,0],
                                                         [0,0,0,1,0,1],
                                                         [1,0,0,0,0,0],
                                                         [0,0,1,0,0,0]]))
        np.testing.assert_array_equal(donationList,np.array([0,1,0,0,0,0]))

    def test_CaseWithTwoDonations(self):
        agentValueations = np.array([[3, 2, 1, 1, 1],
                                     [3, 2, 1, 1, 1], 
                                     [3, 2, 1, 1, 1]])

        bundleAssignemnts = np.array([[1, 1, 1, 0, 0],
                                      [0, 0, 0, 1, 0],
                                      [0, 0, 0, 0, 1]])

        solver = efxSolver.EFXSolver(agentValueations,bundleAssignemnts)
        matching, donationList = solver.findEFX()

        np.testing.assert_array_equal(matching,np.array([[1, 0, 0, 0, 0],
                                                         [0, 0, 0, 1, 0],
                                                         [0, 0, 0, 0, 1]]))
        np.testing.assert_array_equal(donationList,np.array([0,1,1,0,0]))


if __name__ == '__main__':
    unittest.main()
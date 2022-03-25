import unittest
import numpy as np

import efxSolver
import hungarianMethod


class Test(unittest.TestCase):

    def test_VerySimple(self):
        bundleAssignemnts = np.array([[1,0],
                                      [0,1]])
        agentValueations = np.array([[3,2],
                                     [2,3]])

        solver = efxSolver.EFXSolver()
        matching, donationList = solver.findEFX(agentValueations,bundleAssignemnts)
        np.testing.assert_array_equal(matching,np.array([[1,0],[0,1]]))
        np.testing.assert_array_equal(donationList,np.array([0,0]))

    def test_BadAssignmentSimple(self):
        bundleAssignemnts = np.array([[0,1],
                                      [1,0]])
        agentValueations = np.array([[3,2],
                                     [2,3]])

        solver = efxSolver.EFXSolver()
        matching, donationList = solver.findEFX(agentValueations,bundleAssignemnts)
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

        solver = efxSolver.EFXSolver()
        matching, donationList = solver.findEFX(agentValueations,bundleAssignemnts)
        
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

        solver = efxSolver.EFXSolver()
        matching, donationList = solver.findEFX(agentValueations,bundleAssignemnts)
        
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

        solver = efxSolver.EFXSolver()
        matching, donationList = solver.findEFX(agentValueations,bundleAssignemnts)

        np.testing.assert_array_equal(matching,np.array([[1, 0, 0, 0, 0],
                                                         [0, 0, 0, 1, 0],
                                                         [0, 0, 0, 0, 1]]))
        np.testing.assert_array_equal(donationList,np.array([0,1,1,0,0]))

    def test_OneAgentHasAllItems(self):
        agentValueations = np.array([[3, 2, 1, 1, 1],
                                     [3, 2, 1, 1, 1], 
                                     [3, 2, 1, 1, 1]])

        bundleAssignemnts = np.array([[1, 1, 1, 1, 1],
                                      [0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0]])

        solver = efxSolver.EFXSolver()
        matching, donationList = solver.findEFX(agentValueations,bundleAssignemnts)

        np.testing.assert_array_equal(matching,np.array([[1, 0, 0, 0, 0],
                                                         [0, 0, 0, 0, 0],
                                                         [0, 0, 0, 0, 0]]))
        np.testing.assert_array_equal(donationList,np.array([0,1,1,1,1]))
    #
    #   Hungarian test
    #   Remeber that the test uses the order of the matching could start to fail if it is changed
    #   Would maybe not work with the altervativematchingMethod 
    def test_SimpleTestHungarian(self):
        feasibltyMatrix = [[0,15,0],
                           [17,0,0],
                           [0,24,88]]
        solver = hungarianMethod.Solver()
        matching = solver.solveMatchingWithHungarianMethod(feasibltyMatrix)

        np.testing.assert_array_equal(matching,np.array([[2,2],[1,0],[0,1]]))

    def test_LessSimpleTestHungarian(self):
        feasibltyMatrix = np.array([[28, 10, 48, 23, 20],
                                     [17, 18, 49, 20, 15],
                                     [39, 89, 34, 69, 39],
                                     [34, 20, 50, 38, 48],
                                     [23, 92, 4, 93, 12]])

        solver = hungarianMethod.Solver()
        matching = solver.solveMatchingWithHungarianMethod(feasibltyMatrix)
        
        np.testing.assert_array_equal(matching,np.array([[4,3],[3,4],[2,1],[1,2],[0,0]]))


if __name__ == '__main__':
    unittest.main()
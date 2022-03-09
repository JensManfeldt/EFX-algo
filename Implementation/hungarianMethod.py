import numpy as np

class Solver:
    def __init__(self, feasibalityMatrix):
        # make the feasibalityMatrix from java to a np.array hopefully
        self.fm = np.array(feasibalityMatrix)

        self.n = self.fm.shape[0]
    


    def solveMatchingWithHungarianMethod(self,feasibalityMatrix):
        
        # Find min in each row and subtract from each entry in that row
        rowMins = self.fm.min(axis=1)
        self.fm = self.fm.T - rowMins # yikes there must be a better way 

        # Find min in each coloum and subtract
        self.fm = self.fm.T #yikes
        coloumMins = self.fm.min(axis=0)
        self.fm = self.fm - coloumMins

        #Cover 0 with min number of lines not known yet

    
def findMatching(fm):
    
    #find first 0 in row 0 of fm
    for i in range(fm.shape[0]):
        if fm[0,i] == 0:
            matchingPossible, listOfIndexSolutions = findMatchingRec(fm, i)
            if matchingPossible:
                for j in range(len(listOfIndexSolutions)): # Keep trac of the index(s) in the real matrix
                    listOfIndexSolutions[j][0] += 1
                    temp = listOfIndexSolutions[j][1]
                    listOfIndexSolutions[j][1] = temp+1 if temp > i else temp 
                
                listOfIndexSolutions.append([0,i])
                return True, listOfIndexSolutions


def findMatchingRec(fm, coloumIndex):
    fm = np.delete(fm, coloumIndex, axis=1)
    fm = np.delete(fm, 0, axis=0)

    if fm.shape == (1,1):
        if fm[0,0] == 0:
            return True, [[0,0]] # A part of the final matching
        else:
            return False, [[-1,-1]] # Not enculded in the matching
        
    for i in range(fm.shape[0]):
        if fm[0,i] == 0:
            matchingPossible, listOfIndexSolutions = findMatchingRec(fm, i)
            if matchingPossible:
                for j in range(len(listOfIndexSolutions)): # Keep trac of the index(s) in the real matrix
                    listOfIndexSolutions[j][0] += 1
                    temp = listOfIndexSolutions[j][1]
                    listOfIndexSolutions[j][1] = temp+1 if temp > i else temp 
                
                listOfIndexSolutions.append([0,i])
                return True, listOfIndexSolutions
        
    return False, [[-1,-1]] #Not a path with a solution 


feasibltyMatrix = [[0,15,0],[17,0,0],[0,24,88]]

solver = Solver(feasibltyMatrix)

print(findMatching(solver.fm))


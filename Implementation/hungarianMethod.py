import numpy as np

class Solver:
    def __init__(self, feasibalityMatrix):
        # make the feasibalityMatrix from java to a np.array hopefully
        self.fm = np.array(feasibalityMatrix)

        self.n = self.fm.shape[0]
    


    def solveMatchingWithHungarianMethod(self,feasibalityMatrix):
        

        # Step 1 : Find min in each row and subtract from each entry in that row
        rowMins = self.fm.min(axis=1)
        self.fm = self.fm.T - rowMins # yikes there must be a better way 

        # Step 2 : Find min in each coloum and subtract
        self.fm = self.fm.T #yikes
        coloumMins = self.fm.min(axis=0)
        self.fm = self.fm - coloumMins

        #while loop     
        while True:
             # Step 3 : a) Cover 0 with min number of lines not known yet

            coveredRows = []
            coveredColoums = []
            mininal = sum(coveredRows) + sum(coveredColoums)

            # Step 3 b) if minimal = n find matching
            if mininal == self.n:
                return findMatching(self.fm)

            # Step 4 : Create additional 0 if needed
            bestMin = np.infty
            for i in range(self.n):
                for j in range(self.n):
                    if not (coveredRows[i] and coveredColoums[j]):
                        bestMin = np.min(self.fm[i,j], bestMin)
                    
            for i in range(self.n):
                if not coveredRows[i]:
                    self.fm[i,:] -= bestMin
                if coveredColoums[i]:
                    self.fm[:,i] += bestMin


        





    
def findMatching(fm):
    
    #find first 0 in row 0 of fm
    for i in range(fm.shape[0]):
        if fm[0,i] == 0:
            matchingPossible, listOfIndexSolutions = findMatchingRec(fm, i)
            if matchingPossible:
                for j in range(len(listOfIndexSolutions)): # Keep trac of the index(s) in the real matrix
                    listOfIndexSolutions[j][0] += 1
                    temp = listOfIndexSolutions[j][1]
                    listOfIndexSolutions[j][1] = temp+1 if temp >= i else temp 
                
                listOfIndexSolutions.append([0,i])
                return listOfIndexSolutions


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
                    listOfIndexSolutions[j][1] = temp+1 if temp >= i else temp 
                
                listOfIndexSolutions.append([0,i])
                return True, listOfIndexSolutions
        
    return False, [[-1,-1]] #Not a path with a solution 


feasibltyMatrix = [[0,15,0],
                    [17,0,0],
                    [0,24,88]]
feasibltyMatrix2 = [[15,0,0],
                    [0,0,17],
                    [24,0,88]]


solver = Solver(feasibltyMatrix2)

print(findMatching(solver.fm))


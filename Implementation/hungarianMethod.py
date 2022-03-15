from pickletools import read_uint1
import re
import numpy as np

class Solver:
    def __init__(self, feasibalityMatrix):
        # make the feasibalityMatrix from java to a np.array hopefully
        self.fm = np.array(feasibalityMatrix)

        self.n = self.fm.shape[0]

        self.markedRow = np.zeros(self.n)
        self.markedColoum = np.zeros(self.n)
        self.assignedRows = -np.ones(self.n)
        self.zeroesLocationInRow = [] 

    def solveMatchingWithHungarianMethod(self):

        # Step 0 : Convert max problem to min problem 
        # Find max value and subtract each entry from max value
        max = np.max(self.fm)
        self.fm = max - self.fm
        
        print("Step 0 : \n")
        print(self.fm)

        # Step 1 : Find min in each row and subtract from each entry in that row
        for i in range(self.n):
            row = self.fm[i,:]
            row = row - np.min(row)
            
        
        rowMins = self.fm.min(axis=1)
        self.fm = self.fm.T - rowMins # yikes there must be a better way 

        self.fm = self.fm.T #yikes
        print("Step 1: \n")
        print(self.fm)

        # Step 2 : Find min in each coloum and subtract
        
        coloumMins = self.fm.min(axis=0)
        self.fm = self.fm - coloumMins

        print("Step 2: \n")
        print(self.fm)

        #while loop     
        while True:
             # Step 3 : a) Cover 0 with min number of lines not known yet
            
            coveredRows, coveredColoums = self.findMiniamlCover()
            print("Step 3: \n")
            print(self.fm)
            
            print(coveredRows)
            print(coveredColoums)
            minimal = sum(coveredRows) + sum(coveredColoums)

            # Step 3 b) if minimal = n find matching
            print("minimal")
            print(minimal)
            if minimal == self.n:
                # check indexs in result is not 0 in orgianl 
                result = findMatching(self.fm) 
                #print("Result")
                #print(result)
                markedIndexs = []
                for i in range(len(result)):
                    if self.fm[result[i][0],result[i][1]] == 0:
                        markedIndexs.append(i)  
                
                for i in range(len(markedIndexs)-1, -1, -1):
                    temp = result[markedIndexs[i]]
                    if self.fm[temp[0],temp[1]] == 0: # Is not an edge in orginal
                        del result[markedIndexs[i]] 
                    
                return result

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

            
    def findMiniamlCover(self):
        
        crossedColoums = np.zeros(self.n) # False

        for i in range(self.n):
            for j in range(self.n):
                if self.fm[i,j] == 0 and not crossedColoums[j]:
                    self.assignedRows[i] = j 
                    crossedColoums[j] = 1 # True
                    break
            
        for i in range(self.n):
            if self.assignedRows[i] == -1 and not self.markedRow[i]:
                self.markRow(i)
        
        print("Marked Coloum")
        print(self.markedColoum)
        print("marked row")
        print(self.markedRow)
        print("Assigned Row")
        print(self.assignedRows)
        print("covered coloums")
        print(crossedColoums)
        return self.markedColoum, 1 - self.markedRow # python magic

    def markRow(self,rowIndex):
        self.markedRow[rowIndex] = 1
        row = self.fm[rowIndex,:]
        for j in range(self.n):
            if row[j] == 0 and not self.markedColoum[j]:
                self.markColoum(j)

    def markColoum(self,coloumIndex):
        self.markedColoum[coloumIndex] = 1
        coloum = self.fm[:,coloumIndex]
        for i in range(self.n):
            if self.assignedRows[i] == coloumIndex and not self.markedRow[i]:
                self.markRow(i)

    def findMatchingAlternative(self): 
        self.zeroesLocationInRow = [] 

        for i in range(self.n):
            zeroes = []
            for j in range(n):
                if self.fm[i][j] == 0:
                    zeroes.append(j)
            self.zeroesLocationInRow.append(zeroes) 
        
        self.collumTakenBy = np.zeros(self.n)

        self.searchForMatching(0, 0)
  
        results = []
        for j in range (self.n): 
            results.append([self.collumTakenBy[j], j])

        return results


    def searchForMatching(self, row, zeroNumber):
        zeroIndex = self.zeroesLocationInRow[row][zeroNumber]
        if self.collumTakenBy[zeroIndex]:
            if len(self.zeroesLocationInRow[row][zeroNumber]) - 1 > zeroNumber:
                return self.searchForMatching(row, zeroNumber+1)
            else:
                return False
        else: 
            self.collumTakenBy[zeroIndex] = row
            if row + 1 < self.n:
                bool = self.searchForMatching(row + 1, 0)
                if bool: 
                    return True
                else: 
                    self.collumTakenBy[zeroIndex] = 0
                    if len(self.zeroesLocationInRow[row][zeroNumber]) - 1 > zeroNumber:
                        return self.searchForMatching(row, zeroNumber+1)
                    else:
                        return False
            else:
                return True




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
                return listOfIndexSolutions # List of Tuples with coordinates


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
feasibltyMatrix3 = [[0,4,3],
                    [4,0,3],
                    [1,0,0]]

feasibltyMatrix3 = [[0,4,3],
                    [4,0,3],
                    [1,0,0]]

feasibltyMatrix4 = [[108,125,150],
                    [150,135,175],
                    [122,148,250]]

feasibltyMatrix5 = [[17,0,0],
                    [0,15,0],
                    [103,77,0]]

#print(250 - np.array(feasibltyMatrix5))

solver = Solver(feasibltyMatrix4)

#print(findMatching(solver.fm))
print(solver.solveMatchingWithHungarianMethod())

#print(findMatching(solver.fm))


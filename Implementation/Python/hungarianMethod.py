import numpy as np
import sys

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
        fmOrigianl = np.matrix.copy(self.fm)

        # Step 0 : Convert max problem to min problem 
        # Find max value and subtract each entry from max value
        max = np.max(self.fm)
        self.fm = max - self.fm

        # Step 1 : Find min in each row and subtract from each entry in that row
        for i in range(self.n):
            row = self.fm[i,:]
            row = row - np.min(row)
            
        rowMins = self.fm.min(axis=1)
        self.fm = self.fm.T - rowMins 

        self.fm = self.fm.T

        # Step 2 : Find min in each coloum and subtract
        
        coloumMins = self.fm.min(axis=0)
        self.fm = self.fm - coloumMins

        #while loop     
        while True:
             # Step 3 : a) Cover 0 with min number of lines
            coveredRows, coveredColoums = self.findMiniamlCover()
            
            minimal = sum(coveredRows) + sum(coveredColoums)

            # Step 3 b) if minimal = n find matching
            if minimal == self.n:
                result = findMatching(self.fm)

                # check indexs in result is not 0 in orgianl 
                for i in range(len(result)-1, -1, -1):
                    #temp = result[markedIndexs[i]]
                    if fmOrigianl[result[i][0],result[i][1]] == 0: # Is not an edge in orginal
                        del result[i] 

                return result
            
            # Step 4 : Create additional 0 if needed
            bestMin = sys.maxsize # largest interger
            for i in range(self.n):
                for j in range(self.n):
                    if not (coveredRows[i] or coveredColoums[j]):
                        temp = self.fm[i,j]
                        if temp < bestMin: 
                            bestMin = temp

            for i in range(self.n):
                if coveredRows[i] == 0:
                    self.fm[i,:] -= bestMin
                if coveredColoums[i] == 1:
                    self.fm[:,i] += bestMin


    def findMiniamlCover(self):
        crossedColoums = np.zeros(self.n) # False

        self.markedRow = np.zeros(self.n)
        self.markedColoum = np.zeros(self.n)
        self.assignedRows = np.zeros(self.n) -1 

        for i in range(self.n):
            for j in range(self.n):
                if self.fm[i,j] == 0 and crossedColoums[j] == 0:
                    self.assignedRows[i] = j
                    crossedColoums[j] = 1   
                    break  

        for i in range(self.n):
            if self.assignedRows[i] == -1 and self.markedRow[i] == 0:
                self.markRow(i)         

        return 1 - self.markedRow, self.markedColoum # python magic

    def markRow(self,rowIndex):
        self.markedRow[rowIndex] = 1
        row = self.fm[rowIndex,:]
        for j in range(self.n):
            if row[j] == 0 and not self.markedColoum[j]:
                self.markColoum(j)

    def markColoum(self,coloumIndex):
        self.markedColoum[coloumIndex] = 1
        for i in range(self.n):
            if self.assignedRows[i] == coloumIndex and not self.markedRow[i]:
                self.markRow(i)

    def findMatchingAlternative(self): 
        self.zeroesLocationInRow = [] 

        for i in range(self.n):
            zeroes = []
            for j in range(self.n):
                if self.fm[i][j] == 0:
                    zeroes.append(j)
            self.zeroesLocationInRow.append(zeroes) 

        self.collumTakenBy = np.zeros(self.n) -1

        self.searchForMatching(0, 0)
  
        results = []
        for j in range (self.n): 
            results.append([int(self.collumTakenBy[j]), j])

        return results


    def searchForMatching(self, row, zeroNumber):
        zeroIndex = self.zeroesLocationInRow[row][zeroNumber]

        print(self.zeroesLocationInRow[row])
        if self.collumTakenBy[zeroIndex] != -1: 
            if len(self.zeroesLocationInRow[row]) - 1 > zeroNumber:
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
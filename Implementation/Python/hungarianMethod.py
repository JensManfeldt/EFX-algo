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
        
        #print("Step 0 : \n")
        #print(self.fm)

        # Step 1 : Find min in each row and subtract from each entry in that row
        for i in range(self.n):
            row = self.fm[i,:]
            row = row - np.min(row)
            
        
        rowMins = self.fm.min(axis=1)
        self.fm = self.fm.T - rowMins # yikes there must be a better way 

        self.fm = self.fm.T #yikes
        #print("Step 1: \n")
        #print(self.fm)

        # Step 2 : Find min in each coloum and subtract
        
        coloumMins = self.fm.min(axis=0)
        self.fm = self.fm - coloumMins

        #print("Step 2: \n")
        #print(self.fm)

        #while loop     
        while True:
             # Step 3 : a) Cover 0 with min number of lines not known yet
            
            coveredRows, coveredColoums = self.findMiniamlCover()
            #print("Step 3: \n")
            #print(self.fm)
            
            minimal = sum(coveredRows) + sum(coveredColoums)

            # Step 3 b) if minimal = n find matching
            #print("minimal")
            #print(minimal)
            if minimal == self.n:
                
                result = self.findMatchingAlternative()
                #print("Result")
                #print(result)
                # check indexs in result is not 0 in orgianl 
                markedIndexs = []
                for i in range(len(result)):
                    temp = result[i]
                    if self.fm[temp[0],temp[1]] == 0:
                        markedIndexs.append(i)  
                
                for i in range(len(markedIndexs)-1, -1, -1):
                    temp = result[markedIndexs[i]]
                    if fmOrigianl[temp[0],temp[1]] == 0: # Is not an edge in orginal
                        del result[markedIndexs[i]] 
                    
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
        
        #print("\n\n\n")
        #print(self.fm)
        #print("Marked Coloum")
        #print(self.markedColoum)
        #print("marked row")
        #print(self.markedRow)
        #print("Assigned Row")
        #print(self.assignedRows)
        #print("covered coloums")
        #print(crossedColoums)
        #print("\n\n\n")
        return 1 - self.markedRow, self.markedColoum # python magic

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
            for j in range(self.n):
                if self.fm[i][j] == 0:
                    zeroes.append(j)
            self.zeroesLocationInRow.append(zeroes) 
        
        #print("Zeroes Locations")
        #print(self.zeroesLocationInRow)

        self.collumTakenBy = np.zeros(self.n) -1

        self.searchForMatching(0, 0)
  
        results = []
        for j in range (self.n): 
            results.append([int(self.collumTakenBy[j]), j])

        return results


    def searchForMatching(self, row, zeroNumber):
        zeroIndex = self.zeroesLocationInRow[row][zeroNumber]

        #print("Now trying zero:")
        #print(row, zeroIndex)
        
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

feasibltyMatrix6 =[[28, 10, 48, 23, 20],
                   [17, 18, 49, 20, 15],
                   [39, 89, 34, 69, 39],
                   [34, 20, 50, 38, 48],
                   [23, 92, 4, 93, 12]]


#print(250 - np.array(feasibltyMatrix5))

#solver = Solver(feasibltyMatrix6)

#print(findMatching(solver.fm))
#print(solver.solveMatchingWithHungarianMethod())

#print(findMatching(solver.fm))


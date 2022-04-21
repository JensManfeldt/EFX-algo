import numpy as np
import hungarianMethod
import scipy.optimize
import util as u

class EFXSolver: 
        
    def setUp(self, agentsEval, bundleAssigment):
        self.agentsEval = agentsEval
        self.n = agentsEval.shape[0] # number of agents
        self.m = bundleAssigment.shape[1] # number of items
        self.bundleAssigmentZ = np.matrix.copy(bundleAssigment)
        self.bundleAssignmentX = np.matrix.copy(bundleAssigment)
        self.agentEvalOfBundle = agentsEval @ bundleAssigment.T
        self.agentsEFXValueations = np.zeros([self.n,self.n])
        self.t = np.zeros(self.n)
        self.feasibilityGraph = np.zeros([self.n,self.n])
        #self.EFXMaxIndex = -np.ones(self.n)
        self.donationList = np.zeros(self.m,dtype=int)


    def algo1(self, agentsEval, bundleAssigment):

        self.setUp(agentsEval, bundleAssigment)

        self.feasibilityGraph = self.buildFeasibilityGraph()

        while True:

            #matchingSolver = hungarianMethod.Solver()
            #matching = np.array(matchingSolver.solveMatchingWithHungarianMethod(np.matrix.copy(self.feasibilityGraph)))
            copy = np.matrix.copy(self.feasibilityGraph)

            max = np.max(copy)
            copy = max - copy
            row, col = scipy.optimize.linear_sum_assignment(copy)

            matching = []
            for i in range(len(row)):
                matching.append([row[i],col[i]])           
            
            for i in range(len(matching)-1, -1, -1):

                if self.feasibilityGraph[matching[i][0],matching[i][1]] == 0: # Is not an edge in orginal
                    del matching[i]

            if len(matching) == self.n:
                returnMatrix = np.zeros([self.n,self.m]) # Same format as the input 
                for i in range(self.n): # move around rows to match the agent they are assigned to 
                    returnMatrix[matching[i][0],:] = self.bundleAssigmentZ[matching[i][1],:] 

                return returnMatrix,self.donationList
            
            matching = np.array(matching)
            # Find unmatched agent

            unmatchedAgent = -1
            agentsMatched = matching[:,0]
            for i in range(self.n):
               if not (i in agentsMatched):
                   unmatchedAgent = i
                   break

            bundleToTouch, leastValueItemIndex = self.findRobustDemand(unmatchedAgent)

            self.donateItem(leastValueItemIndex,bundleToTouch)

            self.updateValueationsAndUpdateFeasibilityGraph(leastValueItemIndex,bundleToTouch)

    def findEFX(self, agentsEval, bundleAssigment, delta=0, counter=0):     
        allocation, donationlist, isEFX = self.algo2(agentsEval, bundleAssigment, delta)
        if(isEFX):
            return allocation, donationlist, counter
        else: 
            return self.findEFX(agentsEval, allocation, delta, counter + 1)

    def algo2(self, agentsEval, bundleAssigment, delta):
        self.setUp(agentsEval, bundleAssigment)

        self.feasibilityGraph = self.buildFeasibilityGraph()

        while True:

            #matchingSolver = hungarianMethod.Solver()
            #matching = np.array(matchingSolver.solveMatchingWithHungarianMethod(np.matrix.copy(self.feasibilityGraph)))
            copy = np.matrix.copy(self.feasibilityGraph)

            max = np.max(copy)
            copy = max - copy
            row, col = scipy.optimize.linear_sum_assignment(copy)

            matching = []
            for i in range(len(row)):
                matching.append([row[i],col[i]])           
            
            for i in range(len(matching)-1, -1, -1):

                if self.feasibilityGraph[matching[i][0],matching[i][1]] == 0: # Is not an edge in orginal
                    del matching[i]

            if len(matching) == self.n:
                return self.createReturnMatrix(matching),self.donationList, True
            
            matching = np.array(matching)
            # Find unmatched agent

            unmatchedBundle = -1
            bundleMatched = matching[:,1]
            for i in range(self.n):
               if not (i in bundleMatched):
                   unmatchedBundle = i
                   break
            
            itemRemoved = False
            while not itemRemoved:

                path, unmatchedAgent = self.followPath(unmatchedBundle, matching)

                robustDemandBundle, leastValueItemIndex = self.findRobustDemand(unmatchedAgent)

                agentToUnassign = robustDemandBundle

                edgeIndex = -1
                if len(path) != 0:
                    for i in range(len(path)):
                        if robustDemandBundle == path[i,1]:
                            edgeIndex = i
                            break
                    agentToUnassign = path[edgeIndex,0]

                if edgeIndex != -1: # there is an edge to robustbundle on the path    
                    for i in range(len(matching)):
                        if agentToUnassign == matching[i,0]:
                            matching[i,0] = unmatchedAgent # Replace agent matched to robust demand bundle                        
                            break
                else : 

                    self.donateItem(leastValueItemIndex, robustDemandBundle)
                    self.updateValueationsAndUpdateFeasibilityGraph(leastValueItemIndex, robustDemandBundle)

                    currentValueationOfBundle = self.agentEvalOfBundle[robustDemandBundle, robustDemandBundle]
                    orginalValueationOfBundle = sum(self.agentsEval[robustDemandBundle,:] * self.bundleAssignmentX[robustDemandBundle,:])
                    

                    if (2 + delta) * currentValueationOfBundle < orginalValueationOfBundle:
                        self.updateOrginalAlloc(path, robustDemandBundle, unmatchedAgent)
                        return self.bundleAssignmentX, np.zeros(self.m), False

                    

                    itemRemoved = True


    def createReturnMatrix(self,matching):
        returnMatrix = np.zeros([self.n,self.m]) # Same format as the input 
        for i in range(self.n): # move around rows to match the agent they are assigned to 
            returnMatrix[matching[i][0],:] = self.bundleAssigmentZ[matching[i][1],:] 
        return returnMatrix

    def followPath(self, unmatchedBundle, matching):
        agent = unmatchedBundle
        path = []
        for _ in range(len(matching)): 
            for j in range(len(matching)):
                if agent == matching[j,0]:
                    agent = matching[j,1] # setting agent to the agent orginally allocated the bundle that our current agent is allocated
                    path.append(matching[j])
                    break
                 
        return np.array(path), agent

    def updateOrginalAlloc(self, path, robustDemandBundle, lastAgent):

        if len(path) == 0:
            self.bundleAssignmentX[lastAgent,:] = self.bundleAssignmentX[lastAgent,:] + self.bundleAssigmentZ[robustDemandBundle,:]

            robustAgent = robustDemandBundle
            self.bundleAssignmentX[robustAgent,:] -= self.bundleAssigmentZ[robustAgent,:]
            
        else :

            firstAgent = path[0,0]
            self.bundleAssignmentX[firstAgent,:] += self.bundleAssigmentZ[path[0,1],:]

            for i in range(1,len(path)): #range is exclusive
                agent = path[i,0]
                self.bundleAssignmentX[agent,:] = self.bundleAssignmentX[agent,:] - self.bundleAssigmentZ[agent,:] + self.bundleAssigmentZ[path[i,1],:] 

            self.bundleAssignmentX[lastAgent,:] = self.bundleAssignmentX[lastAgent,:] - self.bundleAssigmentZ[lastAgent,:] + self.bundleAssigmentZ[robustDemandBundle,:]

            robustAgent = robustDemandBundle
            self.bundleAssignmentX[robustAgent,:] -= self.bundleAssigmentZ[robustAgent,:]
        

        
            
            
    
    def updateValueationsAndUpdateFeasibilityGraph(self,leastValueItemIndex,robustDemandBundle):       

        affectedAgents = []

        for i in range(self.n):
            maxBundle = int(np.argmax(self.agentsEFXValueations[i,:]))
            if maxBundle == robustDemandBundle:
                affectedAgents.append(i)

        for i in range(self.n):
            self.updateEFXValueationForAgentAndBundle(i,robustDemandBundle)
        
        self.agentEvalOfBundle[:,robustDemandBundle] -= self.agentsEval[:,leastValueItemIndex] # Remove from bundle valueations
        self.updateFeasibilityGraph(robustDemandBundle, affectedAgents)

    def buildFeasibilityGraph(self): 
        
        self.feasibilityGraph = np.zeros([self.n, self.n])

        # Set up agents efx valueations
        for i in range(self.n):
            for j in range(self.n):
                self.updateEFXValueationForAgentAndBundle(i,j)

        # Build initial graph
        for i in range(self.n):  

            efxmaxIndex = int(np.argmax(self.agentsEFXValueations[i,:]))
            efxmax = self.agentsEFXValueations[i,efxmaxIndex]
            originalBundleValuation = self.agentEvalOfBundle[i, i]
            for j in range(self.n):
                if self.agentEvalOfBundle[i,j] >= efxmax and self.agentEvalOfBundle[i,j] > originalBundleValuation:
                    self.feasibilityGraph[i,j] = 1 

            if self.agentEvalOfBundle[i,i] >= efxmax: 
                self.feasibilityGraph[i,i] = pow(self.n, 2)
        
        return self.feasibilityGraph

    def updateEFXValueationForAgentAndBundle(self,agent,bundle):
        leastValuedItem = np.Infinity
        agentValueofItemsInBundle = self.agentsEval[agent,:] * self.bundleAssigmentZ[bundle,:]
        for k in range(self.agentsEval.shape[1]):
            if agentValueofItemsInBundle[k] > 0 and agentValueofItemsInBundle[k] < leastValuedItem:
                leastValuedItem = agentValueofItemsInBundle[k]

        temp = sum(agentValueofItemsInBundle)
        self.agentsEFXValueations[agent,bundle] = temp - leastValuedItem
        


    def findRobustDemand(self,unMatchedAgent):
        
        #bundleToTouch = int(self.EFXMaxIndex[unMatchedAgent])
        bundleToTouch = int(np.argmax(self.agentsEFXValueations[unMatchedAgent,:]))

        
        temp = self.agentsEval[unMatchedAgent,:] * self.bundleAssigmentZ[bundleToTouch,:]
        # np.argmin(np.nonzero(temp)) or argwhere

        leastValuedItemIndex = -1
        leastValuedItem = np.Infinity
        for k in range(self.agentsEval.shape[1]): # find least valued item in bundle j;
            #if temp[k] > 0 and temp[k] < leastValuedItem:
            if self.bundleAssigmentZ[bundleToTouch,k] > 0 and self.agentsEval[unMatchedAgent,k] < leastValuedItem:
                leastValuedItem = temp[k]
                leastValuedItemIndex = k 
        
        return bundleToTouch, leastValuedItemIndex


    def donateItem(self,item, robustDemandBundle):
        self.bundleAssigmentZ[:,item] = 0 # make item leastValueItem part of no bundle

        self.donationList[item] = 1 # Mark item as donated
        
        self.t[robustDemandBundle] = 1

        

    def updateFeasibilityGraph(self,touchedBundle, affectedAgents):
        #print("Updating Feasibility Graph")
        for i in range(self.n): # All agents
            efxmaxIndex = int(np.argmax(self.agentsEFXValueations[i,:]))
            originalBundleValuation = self.agentEvalOfBundle[i, i] 

            if self.feasibilityGraph[i,touchedBundle] != 0: # You wanted the touched bundle, there was an edge
                if i in affectedAgents:    
                    

                        efxmax = self.agentsEFXValueations[i,efxmaxIndex]
                        for j in range(self.n): # Recalc all edges because you have new efxMAX
                            if self.agentEvalOfBundle[i,j] >= efxmax and self.agentEvalOfBundle[i,j] > originalBundleValuation:
                                self.feasibilityGraph[i,j] = pow(self.n,4) if self.t[j] == 1 else 1 
                            else :
                                self.feasibilityGraph[i,j] = 0

                        if self.agentEvalOfBundle[i,i] >= efxmax: # Special Case calc for you orginal bundle
                            self.feasibilityGraph[i,i] = pow(self.n, 4) + pow(self.n, 2) if self.t[i] == 1 else pow(self.n, 2)
                        else :
                            self.feasibilityGraph[i,i] = 0


                else : # You wanted the bundle but it was not your efxmax. Only recalc on touchedbundle 
                    #efxmax = self.agentsEFXValueations[i,int(self.EFXMaxIndex[i])]
                    efxmax = self.agentsEFXValueations[i,efxmaxIndex]                   
                    if self.agentEvalOfBundle[i,touchedBundle] >= efxmax and self.agentEvalOfBundle[i,touchedBundle] > originalBundleValuation:
                        self.feasibilityGraph[i,touchedBundle] = pow(self.n,4)
                    else :
                        self.feasibilityGraph[i,touchedBundle] = 0
        
        # Special handling of agent with touchedbundle as orginal bundle  
        efxmaxIndex = int(np.argmax(self.agentsEFXValueations[touchedBundle]))
        efxmax = self.agentsEFXValueations[touchedBundle,efxmaxIndex]
        originalBundleValuation = self.agentEvalOfBundle[touchedBundle,touchedBundle]
     
        for j in range(self.n): # Recalc edges because of new orginal bundle eval
            if self.agentEvalOfBundle[touchedBundle,j] >= efxmax and self.agentEvalOfBundle[touchedBundle,j] > originalBundleValuation:
                self.feasibilityGraph[touchedBundle,j] = pow(self.n,4) if self.t[j] == 1 else 1
            else :
                self.feasibilityGraph[touchedBundle,j] = 0 
        
        
        # Special case for the touched bundle
        if self.agentEvalOfBundle[touchedBundle,touchedBundle] >= efxmax: 
            self.feasibilityGraph[touchedBundle,touchedBundle] = pow(self.n, 4) + pow(self.n, 2)
        else :
            self.feasibilityGraph[touchedBundle,touchedBundle] = 0
        

values = np.array([[584, 422, 538, 594, 205, 288, 625, 487, 770],
                   [622, 478, 681, 909, 221, 874, 452, 527, 138],
                   [774, 137, 927, 147, 317, 313, 508,  15,  91],
                   [271, 182, 204, 326, 319, 354,  89, 435, 860]])

bundleAssignment = np.array([[0, 1, 0, 0, 0, 0, 1, 0, 1],
                             [0, 0, 0, 1, 0, 1, 0, 0, 0],
                             [1, 0, 1, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 1, 0, 0, 1, 0]])


#bundleAssignment = u.generateBundleAssignmentWithDraftAndVariance(values)

print(bundleAssignment)
solver = EFXSolver()
print(solver.findEFX(values, bundleAssignment))
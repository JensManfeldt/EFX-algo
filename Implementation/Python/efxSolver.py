import numpy as np
import scipy.optimize
import util as u

class EFXSolver: 
        
    def setUp(self, agentsValuations, bundleAssignment):
        self.agentsValuations = agentsValuations
        self.n = agentsValuations.shape[0] # number of agents
        self.m = bundleAssignment.shape[1] # number of items
        self.bundleAssignmentZ = np.matrix.copy(bundleAssignment)
        self.bundleAssignmentX = np.matrix.copy(bundleAssignment)
        self.agentsValuationOfBundle = agentsValuations @ bundleAssignment.T
        self.agentsEFXValuations = np.zeros([self.n,self.n])
        self.setUpEFXValuations()
        self.t = np.zeros(self.n)
        self.feasibilityGraph = np.zeros([self.n,self.n])
        self.donationList = np.zeros(self.m,dtype=int)

    def setUpEFXValuations(self):
        for i in range(self.n):
            for j in range(self.n):
                self.updateEFXValueationForAgentAndBundle(i,j)
                
    def basicAlgorithm(self, agentsEval, bundleAssigment):

        self.setUp(agentsEval, bundleAssigment)

        self.feasibilityGraph = self.buildFeasibilityGraph()

        while True:

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
                    returnMatrix[matching[i][0],:] = self.bundleAssignmentZ[matching[i][1],:] 

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

    def multipleRuns(self, agentsEval, bundleAssigment, delta=0):     
        isEFX = False
        counter = 0
        allocation, donationlist, isEFX = self.advancedAlgorithm(agentsEval, bundleAssigment, delta)

        while not isEFX:
            allocation, donationlist, isEFX = self.advancedAlgorithm(agentsEval, allocation, delta)
            counter += 1

        return allocation, donationlist, counter


    def advancedAlgorithm(self, agentsEval, bundleAssigment, delta=0):
        self.setUp(agentsEval, bundleAssigment)

        self.feasibilityGraph = self.buildFeasibilityGraph()

        while True:

            copy = np.matrix.copy(self.feasibilityGraph)

            row, col = scipy.optimize.linear_sum_assignment(copy,maximize=True)

            matching = []
            for i in range(len(row)):
                matching.append([row[i],col[i]])           
            
            # Find unmatched agent and delete non edges from matching
            unMatchedBundle = -1
            for i in range(len(matching)-1, -1, -1):
                if self.feasibilityGraph[matching[i][0],matching[i][1]] == 0: # Is not an edge in orginal
                    unMatchedBundle = matching[i][1]
                    del matching[i]

            if len(matching) == self.n:
                return self.createReturnMatrix(matching),self.donationList, True
            
            matching = np.array(matching)
            
            itemRemoved = False
            while not itemRemoved:

                path, unmatchedAgent = self.followPath(unMatchedBundle, matching)

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

                    currentValueationOfBundle = self.agentsValuationOfBundle[robustDemandBundle, robustDemandBundle]
                    orginalValueationOfBundle = sum(self.agentsValuations[robustDemandBundle,:] * self.bundleAssignmentX[robustDemandBundle,:])
                    
                    if (2 + delta) * currentValueationOfBundle < orginalValueationOfBundle:
                        self.updateOrginalAlloc(path, robustDemandBundle, unmatchedAgent)
                        return self.bundleAssignmentX, np.zeros(self.m), False

                    itemRemoved = True

    def createReturnMatrix(self,matching):
        returnMatrix = np.zeros([self.n,self.m]) # Same format as the input 
        for i in range(self.n): # move around rows to match the agent they are assigned to 
            returnMatrix[matching[i][0],:] = self.bundleAssignmentZ[matching[i][1],:] 
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
            self.bundleAssignmentX[lastAgent,:] = self.bundleAssignmentX[lastAgent,:] + self.bundleAssignmentZ[robustDemandBundle,:]

            robustAgent = robustDemandBundle
            self.bundleAssignmentX[robustAgent,:] -= self.bundleAssignmentZ[robustAgent,:]
            
        else :

            firstAgent = path[0,0]
            self.bundleAssignmentX[firstAgent,:] += self.bundleAssignmentZ[path[0,1],:]

            for i in range(1,len(path)): #range is exclusive
                agent = path[i,0]
                self.bundleAssignmentX[agent,:] = self.bundleAssignmentX[agent,:] - self.bundleAssignmentZ[agent,:] + self.bundleAssignmentZ[path[i,1],:] 

            self.bundleAssignmentX[lastAgent,:] = self.bundleAssignmentX[lastAgent,:] - self.bundleAssignmentZ[lastAgent,:] + self.bundleAssignmentZ[robustDemandBundle,:]

            robustAgent = robustDemandBundle
            self.bundleAssignmentX[robustAgent,:] -= self.bundleAssignmentZ[robustAgent,:]
         
    def updateValueationsAndUpdateFeasibilityGraph(self,leastValueItemIndex,robustDemandBundle):       

        affectedAgents = []

        for i in range(self.n):
            maxBundle = int(np.argmax(self.agentsEFXValuations[i,:]))
            if maxBundle == robustDemandBundle:
                affectedAgents.append(i)

        for i in range(self.n):
            self.updateEFXValueationForAgentAndBundle(i,robustDemandBundle)
        
        self.agentsValuationOfBundle[:,robustDemandBundle] -= self.agentsValuations[:,leastValueItemIndex] # Remove from bundle valueations
        self.updateFeasibilityGraph(robustDemandBundle, affectedAgents)

    def buildFeasibilityGraph(self): 
        # Build initial graph
        for i in range(self.n):  

            efxmaxIndex = int(np.argmax(self.agentsEFXValuations[i,:]))
            efxmax = self.agentsEFXValuations[i,efxmaxIndex]
            originalBundleValuation = self.agentsValuationOfBundle[i, i]
            for j in range(self.n): 
                if self.agentsValuationOfBundle[i,j] >= efxmax and self.agentsValuationOfBundle[i,j] > originalBundleValuation:
                    self.feasibilityGraph[i,j] = 1 

            if self.agentsValuationOfBundle[i,i] >= efxmax: 
                self.feasibilityGraph[i,i] = pow(self.n, 2)
        
        return self.feasibilityGraph

    def updateEFXValueationForAgentAndBundle(self,agent,bundle):
        leastValuedItem = np.Infinity
        agentValueofItemsInBundle = self.agentsValuations[agent,:] * self.bundleAssignmentZ[bundle,:]
        for k in range(self.agentsValuations.shape[1]):
            if agentValueofItemsInBundle[k] > 0 and agentValueofItemsInBundle[k] < leastValuedItem:
                leastValuedItem = agentValueofItemsInBundle[k]

        temp = sum(agentValueofItemsInBundle)
        self.agentsEFXValuations[agent,bundle] = temp - leastValuedItem
        
    def findRobustDemand(self,unMatchedAgent):
    
        bundleToTouch = int(np.argmax(self.agentsEFXValuations[unMatchedAgent,:]))

        agentsEvalOfItemsInBundle = self.agentsValuations[unMatchedAgent,:] * self.bundleAssignmentZ[bundleToTouch,:]

        leastValuedItemIndex = -1
        leastValuedItem = np.Infinity

        for k in range(self.agentsValuations.shape[1]): # find least valued item in bundle j;
            if self.bundleAssignmentZ[bundleToTouch,k] > 0 and self.agentsValuations[unMatchedAgent,k] < leastValuedItem:
                leastValuedItem = agentsEvalOfItemsInBundle[k]
                leastValuedItemIndex = k 
        
        return bundleToTouch, leastValuedItemIndex

    def donateItem(self,item, robustDemandBundle):
        self.bundleAssignmentZ[:,item] = 0 # make item leastValueItem part of no bundle

        self.donationList[item] = 1 # Mark item as donated
        
        self.t[robustDemandBundle] = 1

    def updateFeasibilityGraph(self,touchedBundle, affectedAgents):
        for i in affectedAgents:
            efxmaxIndex = int(np.argmax(self.agentsEFXValuations[i,:]))
            originalBundleValuation = self.agentsValuationOfBundle[i, i] 

            if self.feasibilityGraph[i,touchedBundle] != 0: # You wanted the touched bundle, there was an edge
                    efxmax = self.agentsEFXValuations[i,efxmaxIndex]
                    for j in range(self.n): # Recalc all edges because you have new efxMAX
                        if self.agentsValuationOfBundle[i,j] >= efxmax and self.agentsValuationOfBundle[i,j] > originalBundleValuation:
                            self.feasibilityGraph[i,j] = pow(self.n,4) if self.t[j] == 1 else 1 
                        else :
                            self.feasibilityGraph[i,j] = 0
                    if self.agentsValuationOfBundle[i,i] >= efxmax: # Special Case calc for you orginal bundle
                        self.feasibilityGraph[i,i] = pow(self.n, 4) + pow(self.n, 2) if self.t[i] == 1 else pow(self.n, 2)
                    else :
                        self.feasibilityGraph[i,i] = 0

            else : # You wanted the bundle but it was not your efxmax. Only recalc on touchedbundle 
                efxmax = self.agentsEFXValuations[i,efxmaxIndex]                   
                if self.agentsValuationOfBundle[i,touchedBundle] >= efxmax and self.agentsValuationOfBundle[i,touchedBundle] > originalBundleValuation:
                    self.feasibilityGraph[i,touchedBundle] = pow(self.n,4)
                else :
                    self.feasibilityGraph[i,touchedBundle] = 0
        
        # Special handling of agent with touchedbundle as orginal bundle  
        efxmaxIndex = int(np.argmax(self.agentsEFXValuations[touchedBundle]))
        efxmax = self.agentsEFXValuations[touchedBundle,efxmaxIndex]
        originalBundleValuation = self.agentsValuationOfBundle[touchedBundle,touchedBundle]
     
        for j in range(self.n): # Recalc edges because of new orginal bundle eval
            if self.agentsValuationOfBundle[touchedBundle,j] >= efxmax and self.agentsValuationOfBundle[touchedBundle,j] > originalBundleValuation:
                self.feasibilityGraph[touchedBundle,j] = pow(self.n,4) if self.t[j] == 1 else 1
            else :
                self.feasibilityGraph[touchedBundle,j] = 0 
                
        # Special case for the touched bundle
        if self.agentsValuationOfBundle[touchedBundle,touchedBundle] >= efxmax: 
            self.feasibilityGraph[touchedBundle,touchedBundle] = pow(self.n, 4) + pow(self.n, 2)
        else :
            self.feasibilityGraph[touchedBundle,touchedBundle] = 0




def findEFX(valueationMatrix):

    bundleAssignment = u.generateBundleAssignmentWithDraft(valueationMatrix)

    solver = EFXSolver()

    alloc, donationList, counter = solver.multipleRuns(valueationMatrix,bundleAssignment)

    return alloc



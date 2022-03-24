import numpy as np
import hungarianMethod

class EFXSolver: 

    def __init__(self, agentsEval, bundleAssigment):
        
        self.agentsEval = agentsEval
        self.n = agentsEval.shape[0] # number of agents
        self.m = bundleAssigment.shape[1] # number of items
        self.bundleAssigment = bundleAssigment
        self.agentEvalOfBundle = agentsEval @ bundleAssigment.T
        self.agentsEFXValueations = np.zeros([self.n,self.n])
        self.t = np.zeros(self.n)
        self.feasibilityGraph = np.zeros([self.n,self.n])
        self.EFXMaxIndex = -np.ones(self.n)
        self.donationList = np.zeros(self.m,dtype=int)

    
    def findEFX(self):

        self.feasibilityGraph = self.buildFeasibilityGraph()

        while True:
            matchingSolver = hungarianMethod.Solver(np.matrix.copy(self.feasibilityGraph))
            matching = np.array(matchingSolver.solveMatchingWithHungarianMethod())

            if len(matching) == self.n:
                returnMatrix = np.zeros([self.n,self.m]) # Same format as the input 
                for i in range(self.n): # move around rows to match the agent they are assigned to 
                    returnMatrix[matching[i,0],:] = self.bundleAssigment[matching[i,1],:] 

                return returnMatrix,self.donationList
        
            # Find unmatched agent
            unmatchedAgent = -1
            agentsMatched = matching[:,0]
            for i in range(self.n):
               if not (i in agentsMatched):
                   unmatchedAgent = i
                   break

            touchedBundle = self.findRobustDemandAndDonate(unmatchedAgent)

            self.t[touchedBundle] = 1

            self.updateFeasibilityGraph(touchedBundle)
            

    def buildFeasibilityGraph(self): 
        
        self.feasibilityGraph = np.zeros([self.n, self.n])

        # Set up agents efx valueations
        for i in range(self.n):
            for j in range(self.n):
                self.updateEFXValueationForAgentAndBundle(i,j)
                self.EFXMaxIndex[i] = np.argmax(self.agentsEFXValueations[i,:])

        # Build initial graph
        for i in range(self.n):  
            efxmax = self.agentsEFXValueations[i,int(self.EFXMaxIndex[i])]
            
            originalBundleValuation = self.agentEvalOfBundle[i, i]
            for j in range(self.n):
                if self.agentEvalOfBundle[i,j] >= efxmax and self.agentEvalOfBundle[i,j] > originalBundleValuation:
                    self.feasibilityGraph[i,j] = 1 

            if self.agentEvalOfBundle[i,i] >= efxmax: 
                self.feasibilityGraph[i,i] = pow(self.n, 2)
        
        return self.feasibilityGraph

    def updateEFXValueationForAgentAndBundle(self,agent,bundle):
        leastValuedItem = np.Infinity
        agentValueofItemsInBundle = self.agentsEval[agent,:] * self.bundleAssigment[bundle,:]
        for k in range(self.agentsEval.shape[1]):
            if agentValueofItemsInBundle[k] > 0 and agentValueofItemsInBundle[k] < leastValuedItem:
                leastValuedItem = agentValueofItemsInBundle[k]
        if self.agentEvalOfBundle.shape[1] == 0:
            leastValuedItem = 0
        self.agentsEFXValueations[agent,bundle] = sum(agentValueofItemsInBundle) - leastValuedItem
        


    def findRobustDemandAndDonate(self,unMatchedAgent):

        bundleToTouch = int(self.EFXMaxIndex[unMatchedAgent])
        temp = self.agentsEval[unMatchedAgent,:] * self.bundleAssigment[bundleToTouch,:]

        leastValuedItemIndex = -1
        leastValuedItem = np.Infinity
        for k in range(self.agentsEval.shape[1]): # find least valued item in bundle j;
            if temp[k] > 0 and temp[k] < leastValuedItem:
                leastValuedItem = temp[k]
                leastValuedItemIndex = k
        
        self.bundleAssigment[:,leastValuedItemIndex] = 0 # make item leastValueItem part of no bundle

        self.donationList[leastValuedItemIndex] = 1 # Mark item as donated

        self.agentEvalOfBundle[:,bundleToTouch] -= self.agentsEval[:,leastValuedItemIndex] # Remove from bundle valueations


        for i in range(self.n): # Update EFX valueation
            self.updateEFXValueationForAgentAndBundle(i,bundleToTouch)
            # We update EFX max index when updateing graph because the old index(s) are needed there 
        
        return bundleToTouch

    def updateFeasibilityGraph(self,touchedBundle):
        
        for i in range(self.n): # All agents

            if self.feasibilityGraph[i,touchedBundle] != 0: # You wanted the touched bundle 
                originalBundleValuation = self.agentEvalOfBundle[i, i] 
                if touchedBundle == self.EFXMaxIndex[i]: # The touched bundle was your efxmax bundle
                    
                    self.EFXMaxIndex[i] = np.argmax(self.agentsEFXValueations[i,:])

                    efxmax = self.agentsEFXValueations[i,int(self.EFXMaxIndex[i])]

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
                    efxmax = self.agentsEFXValueations[i,int(self.EFXMaxIndex[i])]                   
                    if self.agentEvalOfBundle[i,touchedBundle] >= efxmax and self.agentEvalOfBundle[i,touchedBundle] > originalBundleValuation:
                        self.feasibilityGraph[i,touchedBundle] = pow(self.n,4)
                    else :
                        self.feasibilityGraph[i,touchedBundle] = 0
        
        # Special handling of agent with touchedbundle as orginal bundle  
        efxmax = self.agentEvalOfBundle[touchedBundle,int(self.EFXMaxIndex[touchedBundle])]
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





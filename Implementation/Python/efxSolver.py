import numpy as np
import hungarianMethod

class EFXSolver: 

    def __init__(self, agentsEval, bundleAssigment):
        
        self.agentsEval = agentsEval
        self.n = agentsEval.shape[0]
        self.bundleAssigment = bundleAssigment
        self.agentEvalOfBundle = agentsEval @ bundleAssigment.T
        self.agentsEFXValueations = np.zeros([self.n,self.n])
        self.t = np.zeros(self.n)
        self.feasibilityGraph = np.zeros([self.n,self.n])
        self.EFXMaxIndex = -np.ones(self.n)
    
    def findEFX(self):

        print("Agent Valuations of Bundles")
        print(self.agentEvalOfBundle)

        self.feasibilityGraph = self.buildFeasibilityGraph()

        print("FG")
        print(self.feasibilityGraph)

        


        while True:
            matchingSolver = hungarianMethod.Solver(self.feasibilityGraph)
            matching = np.array(matchingSolver.solveMatchingWithHungarianMethod())
            #print(self.feasibilityGraph)
            if len(matching) == self.n: 
                return matching # Someting more has to happen 
        
            unmatchedAgent = -1
            agentsMatched = matching[:,0]
            print("Agents matched")
            print(agentsMatched)
            for i in range(self.n):
               if not (i in agentsMatched):
                   unmatchedAgent = i
                   break

            touchedBundle = self.findRobustDemandAndDonate(unmatchedAgent)

            self.t[touchedBundle] = 1

            self.updateFeasibilityGraph(touchedBundle)
            

    def buildFeasibilityGraph(self): 
        
        self.feasibilityGraph = np.zeros([self.n, self.n])

        for i in range(self.n):
            #efxmax = 0
            originalBundleValuation = self.agentEvalOfBundle[i, i]
            for j in range(self.n):
                leastValuedItem = np.Infinity
                agentValueofItemsInBundle = self.agentsEval[i,:] * self.bundleAssigment[j,:]
                for k in range(self.agentsEval.shape[1]):
                    if agentValueofItemsInBundle[k] > 0 and agentValueofItemsInBundle[k] < leastValuedItem:
                        leastValuedItem = agentValueofItemsInBundle[k]
                self.agentsEFXValueations[i,j] = sum(agentValueofItemsInBundle) - leastValuedItem
                #efxmax = max(efxmax, self.agentsEFXValueation[i,j])
        
            self.EFXMaxIndex[i] = np.argmax(self.agentsEFXValueations[i,:])
            efxmax = self.agentsEFXValueations[i,int(self.EFXMaxIndex[i])]
            
            #print("Efx max for agent: " + str(i))
            #print(efxmax)
            
            for j in range(self.n):
                if self.agentEvalOfBundle[i,j] >= efxmax and self.agentEvalOfBundle[i,j] > originalBundleValuation:
                    self.feasibilityGraph[i,j] = pow(self.n,4) if self.t[j] == 1 else 1 

            if self.agentEvalOfBundle[i,i] >= efxmax: 
                self.feasibilityGraph[i,i] = pow(self.n, 4) + pow(self.n, 2) if self.t[i] == 1 else pow(self.n, 2)
        
        return self.feasibilityGraph

    def findRobustDemandAndDonate(self,unMatchedAgent):
        print("Unmatched agent")
        print(unMatchedAgent)
        bundleRemoveFromIndex = -1
        
        efxMaxForUnMatchedAgentIndex = int(self.EFXMaxIndex[unMatchedAgent])
        temp = self.agentsEval[unMatchedAgent,:] * self.bundleAssigment[efxMaxForUnMatchedAgentIndex,:]

        leastValuedItemIndex = -1
        leastValuedItem = np.Infinity
        for k in range(self.agentsEval.shape[1]): # find least valued item in bundle j;
            if temp[k] > 0 and temp[k] < leastValuedItem:
                leastValuedItem = temp[k]
                leastValuedItemIndex = k

        
        #for j in range(self.n):   
            #leastValuedItemIndex = -1
            #leastValuedItem = np.Infinity
            #temp = self.agentsEval[unMatchedAgent,:] * self.bundleAssigment[j,:]
            #print("Temp for bundle :" + str(j))
            #print(temp)
            ##print("\n")
            #for k in range(self.agentsEval.shape[1]): # find least valued item in bundle j;
            #    if temp[k] > 0 and temp[k] < leastValuedItem:
            #        leastValuedItem = temp[k]
            #        leastValuedItemIndex = k
            #        
            #print("least valued item")
            #print(leastValuedItem)
            #efxValuation = sum(temp) - leastValuedItem
            #if efxValuation > efxmax:
            #    donationItemIndex = leastValuedItemIndex 
            #    efxmax = efxValuation
            #    bundleRemoveFromIndex = j
            

        #print(donationItemIndex)
        
        self.bundleAssigment[:,leastValuedItemIndex] = 0 # make item k part of no bundle

        self.agentEvalOfBundle[:,bundleRemoveFromIndex] -= self.agentsEval[:,leastValuedItemIndex] # Remove from bundle valueations
        print("Bundle assignment")
        print(self.bundleAssigment)
        print("FG")
        print(self.feasibilityGraph)
        for i in range(self.n): # Update EFX valueation
            leastValuedItem = np.Infinity
            agentValueofItemsInBundle = self.agentsEval[i,:] * self.bundleAssigment[bundleRemoveFromIndex,:]
            for k in range(self.agentsEval.shape[1]):
                if agentValueofItemsInBundle[k] > 0 and agentValueofItemsInBundle[k] < leastValuedItem:
                    leastValuedItem = agentValueofItemsInBundle[k]
            self.agentsEFXValueations[i,bundleRemoveFromIndex] = sum(agentValueofItemsInBundle) - leastValuedItem

        return bundleRemoveFromIndex

    def updateFeasibilityGraph(self,touchedBundle):
        
        for i in range(self.n): # All agents

            if self.feasibilityGraph[i,touchedBundle] != 0: # You wanted the touched bundle 
                
                if touchedBundle == self.EFXMaxIndex[i]: # The touched bundle was your efxmax bundle
                    originalBundleValuation = self.agentEvalOfBundle[i, i]
                    self.EFXMaxIndex[i] = np.argmax(self.agentsEFXValueations[i,:])
                    #print(self.EFXMaxIndex[i])
                    efxmax = self.agentsEFXValueations[i,int(self.EFXMaxIndex[i])]

                    for j in range(self.n): # Recalc all edges because you have new efxMAX
                        if self.agentEvalOfBundle[i,j] >= efxmax and self.agentEvalOfBundle[i,j] > originalBundleValuation:
                            self.feasibilityGraph[i,j] = pow(self.n,4) if self.t[j] == 1 else 1 
                        else :
                            self.feasibilityGraph[i,j] = 0
        
                    if self.agentEvalOfBundle[i,i] >= efxmax: # Special Case calc for you orginal bundle
                        self.feasibilityGraph[i,i] = pow(self.n, 4) + pow(self.n, 2) if self.t[i] == 1 else pow(self.n, 2)
                    else :
                        self.feasibilityGraph[i,j] = 0

                else : # You wanted the bundle but it was not your efxmax. Only recalc on touchedbundle                    
                    if self.agentEvalOfBundle[i,touchedBundle] >= efxmax and self.agentEvalOfBundle[i,touchedBundle] > originalBundleValuation:
                        self.feasibilityGraph[i,touchedBundle] = pow(self.n,4)
                    else :
                        self.feasibilityGraph[i,touchedBundle] = 0
        
        # Special handling of agent with touchedbundle as orginal bundle  
        efxmax = self.EFXMaxIndex[touchedBundle]
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



agentsEval = np.array([[1000, 200, 600, 100, 100],
                       [700, 500, 100, 400, 300],
                       [500, 700, 400, 200, 200]])

bundles = np.array([[1, 0, 0, 0, 0],
                    [0, 0, 0, 1, 1],
                    [0, 1, 1, 0, 0]])

agentsEval2 = np.array([[1, 5, 4, 3, 7],
                        [3, 7, 4, 4, 1], 
                        [8, 8, 1, 3, 6], 
                        [2, 1, 9, 2, 3]])

bundles2 = np.array([[0, 0, 0, 0, 1],
                    [0, 1, 1, 0, 0],
                    [1, 0, 0, 0, 0], 
                    [0, 0, 0, 1, 0]])


solver = EFXSolver(agentsEval2, bundles2)
print(solver.findEFX())
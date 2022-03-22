import numpy as np
import hungarianMethod

class EFXSolver: 

    def __init__(self, agentsEval, bundleAssigment):
        
        self.agentsEval = agentsEval
        self.n = agentsEval.shape[0]
        self.bundleAssigment = bundleAssigment
        self.agentEvalOfBundle = agentsEval @ bundleAssigment.T
        self.agentsEFXValueation = np.zeros([self.n,self.n])
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

            if len(matching) == self.n: 
                return matching # Someting more has to happen 
        
            unmatchedAgent = -1
            agentsMatched = matching[:,0]
            for i in range(self.n):
               if not agentsMatched.any() == i:
                   unmatchedAgent = i
                   break

            touchedBundle = self.findRobustDemandAndDonate(unmatchedAgent)

            self.t[touchedBundle] = 1

            self.updateFeasibilityGraph(touchedBundle)
            

    def buildFeasibilityGraph(self): 
        
        efxGraph = np.zeros([self.n, self.n])

        for i in range(self.n):
            #efxmax = 0
            originalBundleValuation = self.agentEvalOfBundle[i, i]
            for j in range(self.n):
                leastValuedItem = np.Infinity
                temp = self.agentsEval[i,:] * self.bundleAssigment[j,:]
                for k in range(self.agentsEval.shape[1]):
                    if temp[k] > 0 and temp[k] < leastValuedItem:
                        leastValuedItem = temp[k]
                self.agentsEFXValueation[i,j] = sum(temp) - leastValuedItem
                #efxmax = max(efxmax, self.agentsEFXValueation[i,j])
        
            self.EFXMaxIndex[i] = np.argmax(self.agentsEFXValueation[i,:])
            efxmax = self.agentsEFXValueation[int(self.EFXMaxIndex[i])]
            
            #print("Efx max for agent: " + str(i))
            #print(efxmax)
            
            for j in range(self.n):
                if self.agentEvalOfBundle[i,j] >= efxmax and self.agentEvalOfBundle[i,j] > originalBundleValuation:
                    efxGraph[i,j] = pow(self.n,4) if self.t[j] == 1 else 1 

            if self.agentEvalOfBundle[i,i] >= efxmax: 
                efxGraph[i,i] = pow(self.n, 4) + pow(self.n, 2) if self.t[i] == 1 else pow(self.n, 2)
        
        return efxGraph

    def findRobustDemandAndDonate(self,unMatchedagent):
        efxmax = 0
        leastValuedItem = np.Infinity
        donationItemIndex = -1
        bundleRemoveFromIndex = -1
        for j in range(self.n):
            temp = self.agentsEval[unMatchedagent,:] * self.bundleAssigment[j,:]
            for k in range(self.agentsEval.shape[1]):
                if temp[k] > 0 and temp[k] < leastValuedItem:
                    leastValuedItem = temp[k]
                    donationItemIndex = k
            efxValuation = sum(temp) - leastValuedItem
            if efxValuation > efxmax: 
                efxmax = efxValuation
                bundleRemoveFromIndex = j

            
        self.bundleAssigment[:,k] = 0 # make item k part of no bundle

        self.agentEvalOfBundle[:,bundleRemoveFromIndex] -= self.agentsEval[:,donationItemIndex] # Remove from bundle valueations

        return bundleRemoveFromIndex

    def updateFeasibilityGraph(self,touchedBundle):
        for i in range(self.n):
            if self.feasibilityGraph[i,touchedBundle] != 0: # You wanted the touched bundle 
                if touchedBundle == self.EFXMaxIndex[i]: # The touched bundle was your favorite
                    originalBundleValuation = self.agentEvalOfBundle[i, i]
                    for j in range(self.n):
                        leastValuedItem = np.Infinity
                        temp = self.agentsEval[i,:] * self.bundleAssigment[j,:]
                        for k in range(self.agentsEval.shape[1]):
                            if temp[k] > 0 and temp[k] < leastValuedItem:
                                leastValuedItem = temp[k]
                        self.agentsEFXValueation[i,j] = sum(temp) - leastValuedItem
                        #efxmax = max(efxmax, self.agentsEFXValueation[i,j])

                    self.EFXMaxIndex[i] = np.argmax(self.agentsEFXValueations[i,:])
                    efxmax = self.agentsEFXValueations[self.EFXMaxIndex[i]]

                    for j in range(self.n):
                        if self.agentEvalOfBundle[i,j] >= efxmax and self.agentEvalOfBundle[i,j] > originalBundleValuation:
                            self.efxGraph[i,j] = pow(self.n,4) if self.t[j] == 1 else 1 
        
                        if self.agentEvalOfBundle[i,i] >= efxmax: 
                            self.efxGraph[i,i] = pow(self.n, 4) + pow(self.n, 2) if self.t[i] == 1 else pow(self.n, 2)
                else : # You wanted the bundle but it was not your favorite
                    
                    if self.agentEvalOfBundle[i,touchedBundle] >= efxmax and self.agentEvalOfBundle[i,touchedBundle] > originalBundleValuation:
                            self.efxGraph[i,touchedBundle] = pow(self.n,4) if i != touchedBundle else pow(self.n,4) + pow(self.n,2)
        
        originalBundleValuation = self.agentEvalOfBundle[touchedBundle,touchedBundle]                
        for j in range(self.n):
            self.efxGraph[i,i] = pow(self.n, 4) + pow(self.n, 2) if self.t[i] == 1 else pow(self.n, 2)



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
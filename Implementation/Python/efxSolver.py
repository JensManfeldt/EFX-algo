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
        self.donationList = np.array([],dtype=int)
        self.DonationCounter = 0
    
    def findEFX(self):

        print("Agent Valuations of Bundles")
        print(self.agentEvalOfBundle)

        self.feasibilityGraph = self.buildFeasibilityGraph()
        


        while True:
            matchingSolver = hungarianMethod.Solver(np.matrix.copy(self.feasibilityGraph))
            matching = np.array(matchingSolver.solveMatchingWithHungarianMethod())
            #print(self.feasibilityGraph)
            if len(matching) == self.n: 
                returnMatrix = np.zeros([self.n,self.n])
                returnMatrix[matching[:,0],matching[:,1]] = 1
                print("ReturnMatrix")
                print(returnMatrix)

                return returnMatrix,self.donationList # Someting more has to happen 
        
            unmatchedAgent = -1
            agentsMatched = matching[:,0]
            print("Agents matched")
            print(agentsMatched)
            for i in range(self.n):
               if not (i in agentsMatched):
                   unmatchedAgent = i
                   break
            self.DonationCounter += 1
            touchedBundle = self.findRobustDemandAndDonate(unmatchedAgent)
            #if self.DonationCounter == 2:
            #    return 
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
                if self.agentEvalOfBundle.shape[1] == 0:
                    leastValuedItem = 0
                self.agentsEFXValueations[i,j] = sum(agentValueofItemsInBundle) - leastValuedItem
                #efxmax = max(efxmax, self.agentsEFXValueation[i,j])
        
            self.EFXMaxIndex[i] = np.argmax(self.agentsEFXValueations[i,:])
            efxmax = self.agentsEFXValueations[i,int(self.EFXMaxIndex[i])]
            
            #print("Efx max for agent: " + str(i))
            #print(efxmax)
            
            for j in range(self.n):
                if self.agentEvalOfBundle[i,j] >= efxmax and self.agentEvalOfBundle[i,j] > originalBundleValuation:
                    self.feasibilityGraph[i,j] = 1 

            if self.agentEvalOfBundle[i,i] >= efxmax: 
                self.feasibilityGraph[i,i] = pow(self.n, 2)
        
        print("EFX max index init")
        print(self.EFXMaxIndex)
        print("Agents EFX Valueations init")
        print(self.agentsEFXValueations)
        return self.feasibilityGraph

    def findRobustDemandAndDonate(self,unMatchedAgent):
        print("Unmatched agent")
        print(unMatchedAgent)
        
        
        bundleToTouch = int(self.EFXMaxIndex[unMatchedAgent])
        temp = self.agentsEval[unMatchedAgent,:] * self.bundleAssigment[bundleToTouch,:]

        leastValuedItemIndex = -1
        leastValuedItem = np.Infinity
        for k in range(self.agentsEval.shape[1]): # find least valued item in bundle j;
            if temp[k] > 0 and temp[k] < leastValuedItem:
                leastValuedItem = temp[k]
                leastValuedItemIndex = k
        
        self.bundleAssigment[:,leastValuedItemIndex] = 0 # make item k part of no bundle

        self.donationList = np.append(self.donationList,leastValuedItemIndex)
        print("donation list")
        print(self.donationList)
        self.agentEvalOfBundle[:,bundleToTouch] -= self.agentsEval[:,leastValuedItemIndex] # Remove from bundle valueations
        #print("Bundle assignment")
        #print(self.bundleAssigment)
        #print("FG")
        #print(self.feasibilityGraph)
        for i in range(self.n): # Update EFX valueation
            leastValuedItem = np.Infinity
            agentValueofItemsInBundle = self.agentsEval[i,:] * self.bundleAssigment[bundleToTouch,:]
            for k in range(self.agentsEval.shape[1]):
                if agentValueofItemsInBundle[k] > 0 and agentValueofItemsInBundle[k] < leastValuedItem:
                    leastValuedItem = agentValueofItemsInBundle[k]
            if leastValuedItem != np.Infinity:
                self.agentsEFXValueations[i,bundleToTouch] = sum(agentValueofItemsInBundle) - leastValuedItem
                # We do update of EFX max index in when updateing graph because the old index(s) are needed
            

        print("EFX max index")
        print(self.EFXMaxIndex)
        print("Agents EFX Valueations After donation")
        print(self.agentsEFXValueations)
        print("Valueation of Bundles")
        print(self.agentEvalOfBundle)
        print("touchedBundle")
        print(bundleToTouch)
        
        return bundleToTouch

    def updateFeasibilityGraph(self,touchedBundle):
        
        for i in range(self.n): # All agents

            if self.feasibilityGraph[i,touchedBundle] != 0: # You wanted the touched bundle 
                originalBundleValuation = self.agentEvalOfBundle[i, i] 
                if touchedBundle == self.EFXMaxIndex[i]: # The touched bundle was your efxmax bundle
                    
                    self.EFXMaxIndex[i] = np.argmax(self.agentsEFXValueations[i,:])
                    #print(self.EFXMaxIndex[i])
                    print("this is agent : " + str(i))
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
        print(efxmax)       
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

agentValueations = np.array([[1, 5, 4, 3, 7, 2],
                                     [3, 7, 4, 4, 1, 8], 
                                     [8, 8, 1, 3, 6, 2], 
                                     [2, 1, 9, 2, 3, 3]])

bundleAssignemnts = np.array([[0, 0, 0, 0, 1, 0],
                                      [0, 1, 1, 0, 0, 0],
                                      [1, 0, 0, 0, 0, 0], 
                                      [0, 0, 0, 1, 0, 1]])


solver = EFXSolver(agentValueations, bundleAssignemnts)
print(solver.findEFX())
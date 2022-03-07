package Implementation;

import java.util.*;

public class EfxFeasibilityGraph {

    int[][] edges;
    int n;
    Agent[] agents;
    Bundle[] bundles;

    public EfxFeasibilityGraph(Agent[] agents, Bundle[] z) {

        this.n = agents.length;
        this.agents = agents;
        this.bundles = z;

        createInitialGraph();

    }

    private void createInitialGraph() {
        edges = new int[n][n]; // remebering weights
        
        for(int a = 0; a < n; a++) {
            int efxValuation = agents[a].getEfxMax();
            int valuationOfOriginalBundle = agents[a].v(bundles[a]); // i == j
            for(int b = 0; b < n ; b++) {
                int valuationOfBundle = agents[a].v(bundles[b]);
                if (valuationOfBundle >= efxValuation & valuationOfBundle > valuationOfOriginalBundle) {
                    edges[a][b] = 1;
                } // definition of edges per paper 
            }
            if(valuationOfOriginalBundle >= efxValuation){
                edges[a][a] = n*n; 
            } // check for i == j 
        }
    }

    public void update(int robustBundleIndex, boolean[] touchedBundles) {

        Bundle touchedBundle = bundles[robustBundleIndex];  

        for(int i = 0 ; i < n ; i++) { // update collum
            if(edges[i][robustBundleIndex] == 0) { // check for exsisting edge 
                continue; // ??? 
            }
            Agent agent = agents[i];
            agent.updateEfxValauationForBundle(touchedBundle);
            int efxMax = agent.getEfxMax(); 
            int valuation = agent.v(touchedBundle);
            if (valuation >= efxMax & valuation > agent.v(bundles[i])) {
                edges[i][robustBundleIndex] = n*n*n*n; // edge to touched bundle now
            }
            else{
                edges[i][robustBundleIndex] = 0; // no longer an edge
            }
        }

        Agent agent = agents[robustBundleIndex];
        int efxMax = agent.getEfxMax();
        int valuationOfOriginalBundle = agent.v(touchedBundle);          
        for(int i = 0 ; i < n ; i++) { // update row
            int valuation = agent.v(bundles[i]);
            if(valuation >= efxMax & valuation > valuationOfOriginalBundle) {
                if(touchedBundles[i]) {
                    edges[robustBundleIndex][i] = n*n*n*n;
                }
                else {
                    edges[robustBundleIndex][i] = 1;
                }
            }                  
        }

        if(valuationOfOriginalBundle >= efxMax) {
            edges[robustBundleIndex][robustBundleIndex] = n*n*n*n + n*n;
        }
        else{
            edges[robustBundleIndex][robustBundleIndex] = 0;
        }

    }

}

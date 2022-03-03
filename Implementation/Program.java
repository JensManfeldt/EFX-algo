package Implementation;
import java.util.*;


// This class will start the algorimthen 
class Program{
    public static void main(String[] args){
        
    }

    public Allocation algorithmeOne(Allocation alloc){

        int n = alloc.getAgents().size(); 

        Bundle[] Z = new Bundle[n]; 
        
        for(Agent a : alloc.getAgents()) {
            Z[a.getNumber()] = alloc.get(a);            
        }

        EfxFeasibilityGraph G = new EfxFeasibilityGraph(alloc.getAgents(), Z); 

        Set<Bundle> T = new HashSet<Bundle>();

        while(true){

            Set<Edge> M = findMatching(G);  

            Set<Agent> agentsMatched = new HashSet<Agent>(); 
            for(Edge e : M) {
                agentsMatched.add(e.getAgent()); 
            }

            if(agentsMatched.size() == n){

                HashMap<Agent, Bundle> temp = new HashMap<>(); 

                for(Edge e :M) {
                    temp.put(e.getAgent(), e.getBundle());
                }

                return new Allocation(temp); 
            }
            
            Agent unmatchedAgent = null;
            for(Agent a :  alloc.getAgents()) {
                if(!agentsMatched.contains(a)) {
                    unmatchedAgent = a;
                    continue; // Stop the loop??? 
                }
            }

            Bundle robustBundle = findRobustDemandAndRemoveItem(unmatchedAgent, Z);

            T.add(robustBundle);

            G.update(robustBundle);

        }

    }

    private Bundle findRobustDemandAndRemoveItem(Agent unmatchedAgent, Bundle[] z) {

        Bundle candidateBundle = z[0]; // Shpuld be something
        Item worstItemInCandidate = null;

        for(int i = 0 ; i < z.length ; i++) {
            Bundle b = z[i]; 
            ArrayList<Item> items = b.getItems(); 
            Item leastValuedItem = items.get(0);
            for(int j = 1 ; j < items.size() ; j++) {
                if(unmatchedAgent.v(items.get(j)) < unmatchedAgent.v(leastValuedItem)) {
                    leastValuedItem = items.get(j);
                }
            }
            if(unmatchedAgent.v(b) - unmatchedAgent.v(leastValuedItem) > unmatchedAgent.v(candidateBundle)) {
                candidateBundle = b;
                worstItemInCandidate = leastValuedItem;
            }   
        }
        
        candidateBundle.removeItem(worstItemInCandidate);

        return candidateBundle;
    }

    private Set<Edge> findMatching(EfxFeasibilityGraph g) {
        return null; 
        // The big cheese
    }
}
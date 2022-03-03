package Implementation;
import java.util.*;


// This class will start the algorimthen 
class Program{
    public static void main(String[] args){
        
    }

    public Allocation algorithmeOne(Allocation alloc){
        HashMap<Agent, Bundle> Z = new HashMap<>(); // need a better solution for ordering
        
        for(Agent a : alloc.getAllocation().keySet()) {
            Z.put(a, alloc.getAllocation().get(a));
        }

        int n = alloc.getAllocation().keySet().size(); 
        
        EfxFeasibilityGraph G = new EfxFeasibilityGraph(Z); 

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
            for(Agent a :  alloc.getAllocation().keySet()) {
                if(!agentsMatched.contains(a)) {
                    unmatchedAgent = a;
                    continue; // Stop the loop??? 
                }
            }

            Bundle robustBundle = findRobustDemandAndRemoveItem(unmatchedAgent, Z);

            T.add(robustBundle);


        }

    }

    private Bundle findRobustDemandAndRemoveItem(Agent unmatchedAgent, HashMap<Agent, Bundle> z) {
        return null;
    }

    private Set<Edge> findMatching(EfxFeasibilityGraph g) {
        return null; 
        // The big cheese
    }
}
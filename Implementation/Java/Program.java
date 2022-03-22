package Implementation;
import java.util.*;


// This class will start the algorimthen 
class Program{
    public static void main(String[] args){
        
    }

    public Allocation algorithmeOne(Allocation alloc){

        int n = alloc.getAgents().size(); 

        Bundle[] Z = new Bundle[n]; 
        Agent[] agents = new Agent[n];
        
        for(Agent a : alloc.getAgents()) {
            int number = a.getNumber();
            agents[number] = a;
            Z[number] = alloc.get(a);            
        }

        EfxFeasibilityGraph G = new EfxFeasibilityGraph(agents, Z); 

        boolean[] touchedBundles = new boolean[n];

        while(true){

            Set<Edge> M = findMatching(G);  // does not end by returning this

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
            for(Agent a :  agents) {
                if(!agentsMatched.contains(a)) {
                    unmatchedAgent = a;
                    continue; // Stop the loop??? 
                }
            }

            int robustBundle = findRobustDemandAndRemoveItem(unmatchedAgent, Z);

            touchedBundles[robustBundle] = true;

            G.update(robustBundle, touchedBundles);

        }

    }

    private int findRobustDemandAndRemoveItem(Agent unmatchedAgent, Bundle[] z) {

        int candidateBundleIndex = 0; // Shpuld be something
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
            if(unmatchedAgent.v(b) - unmatchedAgent.v(leastValuedItem) > unmatchedAgent.v(z[candidateBundleIndex])) {
                candidateBundleIndex = i;
                worstItemInCandidate = leastValuedItem;
            }   
        }
        
        z[candidateBundleIndex].removeItem(worstItemInCandidate);

        return candidateBundleIndex;
    }

    private Set<Edge> findMatching(EfxFeasibilityGraph g) {
        return null; 
        // The big cheese
    }
}
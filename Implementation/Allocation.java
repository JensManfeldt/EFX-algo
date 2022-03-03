package Implementation;
import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashMap;

public class Allocation {
    private HashMap<Agent, Bundle> alloc;

    private ArrayList<Agent> agents;
    private ArrayList<Bundle> bundels;

    public Allocation(){
        this.alloc = new HashMap<Agent,Bundle>();
    }

    public ArrayList<Bundle> getBundels() {
        return bundels;
    }

    public void setBundels(ArrayList<Bundle> bundels) {
        this.bundels = bundels;
    }

    public ArrayList<Agent> getAgents() {
        return agents;
    }

    public void setAgents(ArrayList<Agent> agents) {
        this.agents = agents;
    }

    public Allocation(ArrayList<Agent> agents, ArrayList<Bundle> bundles){
        this.setAgents(agents);
        this.setBundels(bundles);
        this.alloc = new HashMap<>();
        for(int i = 0; i < agents.size(); i++){
            alloc.put(agents.get(i), bundles.get(i));
        }
    }
}

package Implementation;

import java.util.ArrayList;
import java.util.HashMap;

public class Allocation {
    private HashMap<Agent, Bundle> alloc;

    public Allocation(){
        this.alloc = new HashMap<Agent,Bundle>();
    }

    public Allocation(ArrayList<Agent> agents, ArrayList<Bundle> bundles){
        if (agents.size() != bundles.size()) {
            System.out.println("Here Be a Problem");
        }
        this.alloc = new HashMap<>();
        for(int i = 0; i < agents.size(); i++){
            alloc.put(agents.get(i), bundles.get(i));
        }
    }

    public Allocation(HashMap <Agent, Bundle> matching) {
        alloc = matching;
    }

    public HashMap<Agent, Bundle> getAllocation() {
        return alloc;
    }

}

package Implementation;

public class Edge {

    Agent agent;
    Bundle bundle; 

    public Edge(Agent agent, Bundle bundle) {
        this.agent = agent;
        this.bundle = bundle;
    }

    public Agent getAgent() {
        return agent;
    }

    public Bundle getBundle() {
        return bundle;
    }

}

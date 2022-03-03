package Implementation;
import java.util.HashMap;

public class Agent {

    private int number;
    private HashMap<Item,Integer> valueations;

    public Agent(int number){
        this.valueations = new HashMap<>();
        this.number = number;
    }

    public void assignValueToItem(Item i, int value){
        valueations.put(i, value);
    }

    public int v(Item i){
        return valueations.get(i);
    }
    
    public int v(Bundle b){
        int total = 0;
        for(Item i: b.getItems()){
            total += v(i);
        }
        return total;
    }

    public int getNumber() {
        return number;
    }

    
}

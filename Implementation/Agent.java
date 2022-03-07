package Implementation;
import java.util.*;

public class Agent {

    private int number;
    private HashMap<Item, Integer> valueations;
    private HashMap<Bundle, Integer> bundlesEfxValuations;

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

    private int efxValuation(Bundle bundle) {
        List<Item> items = bundle.getItems();
        int min = 0; 
        for(Item item : items){
            min = Math.min(min, v(item));
        } 
        return v(bundle) - min;  
    }

    public void createEfxValuations(Bundle[] bundles) {
        for(Bundle b : bundles) {
            bundlesEfxValuations.put(b, efxValuation(b));
        }
    }

    public void updateEfxValauationForBundle(Bundle b) {
        bundlesEfxValuations.put(b, efxValuation(b));
    }

    public int getEfxMax() {
        return Collections.max(bundlesEfxValuations.values());
    }
    
}

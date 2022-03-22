package Implementation;
import java.util.ArrayList;

public class Bundle {
    private ArrayList<Item> items;

    public Bundle(){
        this.items = new ArrayList<>();
    }

    public Bundle(ArrayList<Item> items){
        this.items = items;
    }

    public ArrayList<Item> getItems() {
        return items;
    }

    public void putItemInBundle(Item i){
        items.add(i);
    }

    public void removeItem(Item i){
        items.remove(i);
    }

    public void setBundle(ArrayList<Item> items){
        this.items = items;
    }

}

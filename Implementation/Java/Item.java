package Implementation;

public class Item {

    int number; 
    String name;
    String describtion; 

    public Item(int number){
        this.number = number;
        name = "";
        describtion = "";
    }

    public Item(int number, String name, String describtion) {
        this.number = number;
        this.name = name;
        this.describtion = describtion;
    }

}

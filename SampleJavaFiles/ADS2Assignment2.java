package adsassignment2;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.Calendar;
import java.util.Date;
import java.util.Scanner;
import javax.swing.JFrame;

/**
 * @author b2017532
 */
public class ADS2Assignment2 {

    public static void main(String[] args) {
        //XMLParser parse = new XMLParser();
        XMLParse parse = new XMLParse();
        TagNode root = new TagNode();
        menu(root, parse);

    }

    public static void menu(TagNode root, XMLParse parse){
        Scanner input = new Scanner(System.in);

        int option = 1;
        while(option != 0){
            printMenu();
            option = input.nextInt();
            switch (option){
                case 1: System.out.println("Parsed XML file");
                        root = parse.start();
                        break;
                case 2: System.out.println("Printing XML tree");
                        root.printFile(root,0);
                        break;
                case 3: System.out.println("Modifying XML file");
                        milestoneEdit(root,false);
                        break;
                case 4: System.out.println("Extrtacting names and rs elements");
                        String[] names = new String[0]; //array to hold the list of names
                        names = extractNames(root,false,names);
                        writeNames(names);
                        placeKeys(root);
                        break;
                case 5: System.out.println("Write to new file");
                        System.out.println("Have edits taken place? 1 if yes");
                        if (input.nextInt() == 1){
                            System.out.println("Author of the changes?");
                            Scanner authorInput = new Scanner(System.in);
                            String author = authorInput.nextLine();
                            addRevisions(root,false,author);
                        }
                        PrintWriter writer;
                        try {
                            writer = new PrintWriter("Froissart1-Result.xml");
                            root.printFile(root,0,writer);
                            writer.close();
                        } catch (FileNotFoundException ex) {
                            System.out.println(ex);
                        }
                        break;
                case 6: searchTree(root);
                        break;
                case 0: System.out.println("Terminating program");
                        break;
                default: System.out.println("Invalid input");
                        break;
            }
        }
    }

    public static void printMenu(){
        System.out.println("\nMain Menu");
        System.out.println();
        System.out.println("1. Parse XML file");
        System.out.println("2. Print XML tree");
        System.out.println("3. Modify Milestone elements");
        System.out.println("4. Extract names and insert keys (Keys not done yet)");
        System.out.println("5. Write current data to new file");
        System.out.println("6. Search the tree(extra)");
        System.out.println("0. Terminate");
    }

    public static void milestoneEdit(TagNode root, boolean inText){
        int i = 0;
        if (inText && "milestone".equals(root.name)){
            //System.out.print("Found\t");
            int count = 0;
            String nValue = null;
            String edValue = null;
            for (int j = 0; j < root.noOfAttributes; j++){  //go through all nodes checking for ed and n attributes
                if(root.attributes[j].name.equals("ed")){   //get ed value
                    edValue = root.attributes[j].value;
                }
                if(root.attributes[j].name.equals("n")){    //get n value
                    nValue = root.attributes[j].value;
                }
            }
            if (nValue != null && edValue != null){
                System.out.println("BookI-Translaation_"+edValue+"_"+nValue);
                AttributeNode attr = new AttributeNode();
                attr.name="xml:id";
                attr.value="BookI-Translaation_"+edValue+"_"+nValue;
                root.addAttribute(attr);
            }
        }
        System.out.println("debug");
        while (i < 12 && root.child[i] != null){
            if (root.name.equals("text")){   //find the text block
                inText = true;
            }
            milestoneEdit(root.child[i], inText); //recursivly go through until all children explored
            i++;
        }
    }

    public static String[] extractNames(TagNode root, boolean inText, String[] names){
        if ((root.name.equals("name") || root.name.equals("rs"))&& inText){    //inText ensures it only pulls names from within the text tag
            if (checkNames(names,root.data)){
                String[] temp = new String[names.length+1];
                System.arraycopy(names, 0, temp, 0, names.length);
                names = temp;
                names[names.length-1] = root.data;
            }
        }
        int i = 0;
        while (i < 12 && root.child[i] != null){
            if (root.name.equals("text")){   //find the text block
                inText = true;
            }
            names = extractNames(root.child[i], inText, names); //recursivly go through until all children explored
            i++;
        }
        return names;
    }

    public static boolean checkNames(String[] names, String name){
        for(int i=0;i<names.length; i++){
            if(name.equals(names[i])){
                //System.out.println("Checking: "+name+" against "+names[i]);
                return false;
            }
        }
        return true;
    }

    public static void writeNames(String[] names){
        try{
            StringBuilder nameLong = new StringBuilder(250);
            System.out.println("Printing names!");
            PrintWriter write;
            write = new PrintWriter("names.txt");   //print all found name attributes to a txt file
            for (int j = 0; j < names.length; j++){
                //System.out.println("Name: "+names[j]);
                write.write(j+".\t"+names[j]+'\n');         //new line is seperator for names
                nameLong.append(j+". "+names[j]+"<br>");
            }
            write.close();
            //test gui = new test(nameLong.toString());
            //gui.setDefaultCloseOperation(JFrame.HIDE_ON_CLOSE);
            //gui.setSize(275,800);
            //gui.setVisible(true); //gui to output names
        } catch(FileNotFoundException ex) {
            System.out.println(ex);
        }

    }

    public static void placeKeys(TagNode root){
        try{
            String[] names = extractNames();
            keys(root,false,names);
        }catch (Exception ex) {
            System.out.println(ex);
        }
    }

    public static String[] keys(TagNode root, boolean inText, String[] names){
        if ((root.name.equals("name") || root.name.equals("rs") )&& inText){    //inText ensures it only pulls names from within the text tag
            //place the key
            for(int i=0; i < names.length-1;i++){ //go through to find the corresponding name
                //System.out.println(i+"  "+root.data+" = "+names[i]+"@");
                //System.out.println(names[i].substring(1));
                if(names[i] != null && names[i].substring(1, names[i].length()-1).equals(root.data)){
                    //System.out.println(root.data);
                    AttributeNode newAttr = new AttributeNode();
                    newAttr.name = "key";
                    newAttr.value = Integer.toString(i);
                    root.addAttribute(newAttr);
                    //System.out.println(newAttr.name+" # "+newAttr.value);
                }
            }
        }
        int i = 0;
        while (i < 12 && root.child[i] != null){
            //System.out.println("calling");
            if (root.name.equals("text")){   //find the text block
                inText = true;
            }
            keys(root.child[i], inText, names); //recursivly go through until all children explored
            i++;
        }
        return names;
    }

    public static String[] extractNames(){
        try{
            FileInputStream nameFile = new FileInputStream("names.txt");
            System.out.println("Printing key values from file");
            char current = ' ';
            String names[] = new String[35];
            int i = 0;
            while(current != (char) -1){    //pull the names out of the names.txt file
                StringBuffer keyValue = new StringBuffer(3);
                StringBuffer keyName = new StringBuffer(50);
                while (current != '.'){
                    keyValue.append(current);
                    current = (char) nameFile.read();
                }
                while(current != '\n'){
                    current = (char) nameFile.read();
                    keyName.append(current);
                }
                //System.out.print(keyValue.toString()+keyName.toString());
                names[i] = keyName.toString();
                i++;
                current = (char) nameFile.read();
            }
            nameFile.close();
            return names;
        }catch (Exception ex) {
            System.out.println(ex);
        }
        return null;
    }

    public static boolean cleanData(StringBuffer string){
        if (string.charAt(1) == ' ') {
            return false;
        }
        return true;
    }

    public static void addRevisions(TagNode root, boolean complete, String user){
        if (root.name.equals("revisionDesc")){
            TagNode change = new TagNode(); //create the new tags
            TagNode date = new TagNode();
            TagNode name = new TagNode();
            change.name = "change";
            date.name = "date";
            name.name = "name";
            change.child[0] = date;     //should probably have used a constructor with parameters...
            change.child[1] = name;
            date.parent = change;       //sort the links out between the tags
            name.parent = change;
            change.parent = root;
            int i = 0;
            while(root.child[i] != null){
                i++;
            }
            root.child[i] = change;
            AttributeNode key = new AttributeNode();    //sort the attributes out
            AttributeNode type = new AttributeNode();
            type.name = "type";
            type.value = "program";
            key.name = "key";

            Calendar cal = Calendar.getInstance();  //get the current date
            Date dateWithoutTime = cal.getTime();
            date.data = dateWithoutTime.toString();
            name.data = user;
            change.data = "Milestone xml:id attribute added, key attribute added to name and rs tags";

            i = 0;
            StringBuffer keyBuffer = new StringBuffer(5);
            while(i < name.data.length()){      //extract only the initials
                if(i == 0){
                    keyBuffer.append(name.data.charAt(i));
                }
                else if(name.data.charAt(i-1) == ' '){
                    keyBuffer.append(name.data.charAt(i));
                }
                i++;
            }
            key.value = keyBuffer.toString();
            name.addAttribute(type);    //add the attributes to the tags
            name.addAttribute(key);
            complete = true;
        }
        int i = 0;
        while (!complete && i < 12 && root.child[i] != null){
            addRevisions(root.child[i], complete, user);
            i++;
        }
    }

    public static void searchTree(TagNode root){
        boolean upper = false;
        System.out.println("Searching the tree");
        if(!root.name.equals("null")){
            Scanner input = new Scanner(System.in);
            System.out.println("please enter your search term");
            String searchTerm = input.nextLine();
            System.out.println("Match case? y/n");
            char caseOpt = input.next().charAt(0);
            if(caseOpt != 'y'){
                searchTerm = searchTerm.toUpperCase();
                upper = true;
            }
            System.out.println("Search started using: "+searchTerm);
            search(root, searchTerm, false, false, upper);
        }
        else {
            System.out.println("Tree is empty!");
        }
    }

    public static boolean search(TagNode root, String searchTerm, boolean found1, boolean found2, boolean upper){
        if(found1 || found2){
            return true;
        }
        else if(!upper){
            searchName(root,searchTerm,found1);
            searchData(root,searchTerm,found2);
        }
        else if(upper){
            searchNameUpper(root,searchTerm,found1);
            searchDataUpper(root,searchTerm,found2);
        }
        int i = 0;
        while(i <12 && root.child[i] != null && !found1){
            found1 = search(root.child[i], searchTerm, found1, found2, upper); //recursivly go through until all children explored
            i++;
        }
        if (found1 || found2){
            return true;
        }
        else{
            return false;
        }
    }

    public static void searchName(TagNode root, String searchTerm, boolean found){
        if(searchTerm.length() < root.name.length()){
            for(int i = 0; i <= root.name.length()-searchTerm.length();i++){
                if(root.name.substring(i,i+searchTerm.length()).equals(searchTerm)){
                    System.out.println("Found: "+searchTerm);
                    found = true;
                    printSearch(root, searchTerm);
                    root.printFile(root,0);
                }
                else {
                    //System.out.println(root.name.substring(i,i+searchTerm.length())+" != "+searchTerm);
                }
            }
        }
        else {
            if(root.name.equals(searchTerm)){
                found = true;
                System.out.println("Found: "+searchTerm);
                printSearch(root,searchTerm);
                root.printFile(root,0);
            }
            else {
                //System.out.println(root.name+" != "+searchTerm);
            }
        }
    }

    public static void searchData(TagNode root, String searchTerm, boolean found){
        if(!root.selfClosing){
            if(searchTerm.length() < root.data.length()){
                for(int i = 0; i <= root.data.length()-searchTerm.length();i++){
                    if(root.data.substring(i,i+searchTerm.length()).equals(searchTerm)){
                        System.out.println("Found: "+searchTerm);
                        found = true;
                        printSearch(root, searchTerm);
                        root.printFile(root,0);
                    }
                    else {
                        //System.out.println(root.name.substring(i,i+searchTerm.length())+" != "+searchTerm);
                    }
                }
            }
            else {
                if(root.data.equals(searchTerm)){
                    found = true;
                    System.out.println("Found: "+searchTerm);
                    printSearch(root,searchTerm);
                    root.printFile(root,0);
                }
                else {
                    //System.out.println(root.name+" != "+searchTerm);
                }
            }
        }
    }

    public static void searchNameUpper(TagNode root, String searchTerm, boolean found){
        if(searchTerm.length() < root.name.length()){
            for(int i = 0; i <= root.name.length()-searchTerm.length();i++){
                if(root.name.substring(i,i+searchTerm.length()).toUpperCase().equals(searchTerm)){
                    System.out.println("Found: "+searchTerm);
                    found = true;
                    printSearch(root, searchTerm);
                    root.printFile(root,0);
                }
                else {
                    //System.out.println(root.name.substring(i,i+searchTerm.length())+" != "+searchTerm);
                }
            }
        }
        else {
            if(root.name.toUpperCase().equals(searchTerm)){
                found = true;
                System.out.println("Found: "+searchTerm);
                printSearch(root,searchTerm);
                root.printFile(root,0);
            }
            else {
                //System.out.println(root.name+" != "+searchTerm);
            }
        }
    }

    public static void searchDataUpper(TagNode root, String searchTerm, boolean found){
        if(!root.selfClosing){
            if(searchTerm.length() < root.data.length()){
                for(int i = 0; i <= root.data.length()-searchTerm.length();i++){
                    if(root.data.substring(i,i+searchTerm.length()).toUpperCase().equals(searchTerm)){
                        System.out.println("Found: "+searchTerm);
                        found = true;
                        printSearch(root, searchTerm);
                        root.printFile(root,0);
                    }
                    else {
                        //System.out.println(root.name.substring(i,i+searchTerm.length())+" != "+searchTerm);
                    }
                }
            }
            else {
                if(root.data.toUpperCase().equals(searchTerm)){
                    found = true;
                    System.out.println("Found: "+searchTerm);
                    printSearch(root,searchTerm);
                    root.printFile(root,0);
                }
            }
        }
    }

    public static void printSearch(TagNode root, String searchTerm){
        System.out.println("Your search term was: "+searchTerm);
        System.out.println("It was found in: <"+root.name+">");
        System.out.println("The data of the tag is: \n\t"+root.data);
    }
}

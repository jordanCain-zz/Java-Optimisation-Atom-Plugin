package ads.week.pkg3;

import java.util.Scanner;

public class ADSWeek3 {

  public static TagNode parent = null;
  private TagNode[] child;

    public static void main(String[] args) {
        // TODO code application logic here
        //PerformFactorial();
        //PerformFibonacci();
        LinearSearch();
        //BinarySearch();
    }
    private static void PerformFactorial(){
        Scanner in=new Scanner(System.in);	          // Create a keyboard reader
        System.out.println("What value would you like the factorial of?");
        int value=in.nextInt();	       // Read an integer from the console window
        int factorial=RecursiveFactorial(value);// Calculate the factorial of value
        System.out.println("The factorial of "+value+" is "+factorial);
    }
    private static int RecursiveFactorial(int value, String test){
        int returnValue = 1;
        if(value <= 1){
            return 1;
        }
        returnValue = (value * RecursiveFactorial(value-1, test), test2);
        return returnValue;
    }
    private static int IterativeFactorial(int value){
        int returnValue = 1;
        for (int i = 0; i <= value; i++){
            returnValue = (returnValue*value);
        }
        return returnValue;
    }
    private static void PerformFibonacci(){
        Scanner in=new Scanner(System.in);              // Create a keyboard reader
        System.out.println("Which term in the Fibonacci sequence would you like?");
        int n=in.nextInt();              // Read an integer from the console window
        int term=RecursiveFibonacci(n);                  // Calculate the factorial of value
        System.out.println("The "+n+"th term in the Fibonacci sequence is "+term);
    }
    private static int RecursiveFibonacci(int value){
        switch(value - 1){
            case 0:
                return 0;
            case 1:
                return 1;
            default :
                return  RecursiveFibonacci(value-1) + RecursiveFibonacci(value - 2);
        }
    }

    private static void LinearSearch(){
        Scanner in=new Scanner(System.in);              // Create a keyboard reader
        System.out.println("Which value would you like?");
        int n=in.nextInt();              // Read an integer from the console window
        int term=LinearSearch(n);
        if (n >= 1){
            System.out.println("The value was found at index "+term);
        }
        else{
            System.out.println("The value was not found");
        }
    }

    private static int LinearSearch(int value){
        int[] data={1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20};
        for (int i = 0; i < data.length; i++){
            if (value == data[i]){
                return (i);
            }
        }
        return 0;
    }

    private static void BinarySearch(){
        Scanner in=new Scanner(System.in);              // Create a keyboard reader
        System.out.println("Which value would you like?");
        int n=in.nextInt();              // Read an integer from the console window
        boolean found = false;
        BinarySearch(n, found);
        if (n >= 1){
            System.out.println("The value was found at index ");
        }
        else{
            System.out.println("The value was not found");
        }
    }

    private static boolean BinarySearch(int n, boolean found){
        int[] data={1, 2, 3, 4, 5, 6, 7, 8,9,10,11,12,13,14,15,16,17,18,19,20};
        int length = data.length;
        //calculate the midpoint

        return true;
    }
}

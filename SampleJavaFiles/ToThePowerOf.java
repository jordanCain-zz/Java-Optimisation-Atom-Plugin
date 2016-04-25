package tothepowerof;

public class ToThePowerOf {

  private int test;

    public static void main(String[] args) {
        System.out.println(square(2));
        System.out.println(cube(2));
        System.out.println(quart(2));
    }

    public static int square(int value) {
      int returnVal = value;
      for(int i = 0; i < 1; i++){
        returnVal = value * value;
      }
      return returnVal;
    }

    public static int cube(int value) {
      int returnVal = value;
      for(int i = 0; i < 2; i++){
        returnVal = returnVal * value;
      }
      return returnVal;
    }

    public static int quart(int value) {
      int returnVal = value;
      for(int i = 0; i < 3; i++){
        returnVal = returnVal * value;
      }
      return returnVal;
    }
}

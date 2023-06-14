import org.junit.Test;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;
import static org.junit.jupiter.api.Assertions.assertEquals;
import java.io.File;  // Import the File class
import java.io.FileNotFoundException;  // Import this class to handle errors
import java.util.Scanner; // Import the Scanner class to read text files

public class IntegerToRoman   
{  
//method to convert integer to roman  
//function that converts integer to roman  
    public static String intToRoman(int number)   
    {  
        //creating array of place values      
        String[] thousands = {"", "M", "MM", "MMM", "MMMM"};  
        String[] hundreds = {"", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"};  
        String[] tens = {"", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"};  
        String[] units = {"", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"};  
        return thousands[number / 1000] + hundreds[(number % 1000) / 100] + tens[(number % 100) / 10] + units[number % 10];  
    }  
    public static void main(String args[])   
    {  
    //creating an array of integers to be convert into roman      
        int[] numbers = {13, 21, 38, 50, 190, 141, 117, 120, 125, 138, 149, 6, 712, 181, 197, 918, 199, 1100, 1101, 1248, 1253};  
        for (int number : numbers)   
            {  
            System.out.printf("%4d -> %8s\n", number, intToRoman(number));  
            }  
    }
    
    @Test
    public void test_from_file(){
        try{
            File myObj = new File("zadt_output.txt");
            Scanner myReader = new Scanner(myObj);
            int i = 1;
            while(myReader.hasNextLine()){
                String data = myReader.nextLine();
                System.out.println(data);
                assertEquals(data, intToRoman(i));
                i++;
            }
            myReader.close();
            System.out.println("Test passed i = " + i);
            assertEquals(i,4000);
        }
        catch (FileNotFoundException e) {
        System.out.println("An error occurred.");
        e.printStackTrace();
        }
    }
}

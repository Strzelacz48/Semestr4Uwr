import org.junit.Test;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;
import static org.junit.jupiter.api.Assertions.assertEquals;
import java.io.File;  // Import the File class
import java.io.FileNotFoundException;  // Import this class to handle errors
import java.util.Scanner; // Import the Scanner class to read text files
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.api.extension.ExtensionContext;
import org.junit.jupiter.api.extension.ParameterContext;

public class z3
{
    public static String intToRoman(int number)   
    {  
        //creating array of place values      
        String[] thousands = {"", "M", "MM", "MMM", "MMMM"};  
        String[] hundreds = {"", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"};  
        String[] tens = {"", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"};  
        String[] units = {"", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"};  
        return thousands[number / 1000] + hundreds[(number % 1000) / 100] + tens[(number % 100) / 10] + units[number % 10];  
    }  
    //Napisz własne rozszerzenie dla JUnit 5. Rozszerzenie ma wstrzykiwać do metody testowej
    //jako napis zawartość pliku, ścieżka do którego jest podana jako argument adnotacji. 

    @Test
    @ExtendWith(FileContentExtension.class)
    void test(@FileExtention.File(path = "zadt_output.txt") String content)
    {
        String[] numbers = content.split(" ");
        int i = 1;
        for(String number : numbers){
            assertEquals(number, intToRoman(i));
            i++;
        }

        System.out.println(content);
    }
}
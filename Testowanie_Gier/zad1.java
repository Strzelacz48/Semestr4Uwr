import java.util.Scanner;
import java.util.List;
import java.util.stream.Collectors;
import java.util.Arrays;

public class zad1 {
    public class dowolna{
        public List<String> funkcja1(List<String> lista, String slowo){
            return lista.stream().filter(s -> !s.contains(slowo)).collect(Collectors.toList());
        }

    } 
    public static void main(String[] args) {

        // Creates a reader instance which takes
        // input from standard input - keyboard
        List<String> supplierNames = Arrays.asList("Ala", "ma", "kota");
        dowolna d = new dowolna();
        System.out.println(d.funkcja1(supplierNames, "ma"));
        
    }
}
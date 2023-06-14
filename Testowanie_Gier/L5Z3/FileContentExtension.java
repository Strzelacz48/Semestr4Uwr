import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class FileContentExtension {
    //napisz klasę która przyjmuje ścieżkę do pliku jako argument konstruktora
    //i ma metodę która zwraca zawartość pliku jako napis

    String path;
    public FileContentExtension(String path){
        this.path = path;
    }

    public String file_content()
    {
        String result = "";
        try{
            File myObj = new File(path);
            Scanner myReader = new Scanner(myObj);
            
            while(myReader.hasNextLine()){
                String data = myReader.nextLine();
                result += " " + data;
            }
            myReader.close();
        }
        catch (FileNotFoundException e) {
        System.out.println("An error occurred.");
        e.printStackTrace();
        }
        return result;
    }
}

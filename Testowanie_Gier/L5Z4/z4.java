import java.util.Scanner;
import java.lang.Math;
//import test
import org.junit.Test;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;
import static org.junit.jupiter.api.Assertions.assertEquals;
import java.util.Arrays;
import java.util.Collection;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.DynamicTest.dynamicTest;

public class z4{
    //zwraca 3 dla równobocznego trójkąta, 2 dla równoramiennego, 1 dla różnobocznego, 0 dla nie trójkąta
    public int is_a_triangle(float x1, float y1, float x2, float y2, float x3, float y3)
    {
        float a = (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2);
        float b = (x1-x3)*(x1-x3) + (y1-y3)*(y1-y3);
        float c = (x2-x3)*(x2-x3) + (y2-y3)*(y2-y3);
        if ((a+b==c || a+c==b || b+c==a) && ((x1 - x2)*(y1 - y3) != (x1 - x3)*(y1 - y2)))
            if(a==b && a==c && b==c)
                return 3;
            else if(a==b || a==c || b==c)
                return 2;
            else
                return 1;
        else
            return 0;
    }

    @Test//dynamiczne testy
    public void test1(){
        assert is_a_triangle(0,0,0,0,0,0) == 0;
    }
    
    @TestFactory
    public DynamicTest[] test2(){
        return new DynamicTest[]{
                DynamicTest.dynamicTest("test2", () -> assertEquals(2, is_a_triangle(0,0,0,1,1,0))),
                DynamicTest.dynamicTest("test3", () -> assertEquals(2, is_a_triangle(0,0,0,2,2,0))),
                DynamicTest.dynamicTest("test4", () -> assertEquals(1, is_a_triangle(0,0,3,0,0,1))),
                DynamicTest.dynamicTest("test5", () -> assertEquals(1, is_a_triangle(0,0,-3,0,0,-2)))
        };
    }
}

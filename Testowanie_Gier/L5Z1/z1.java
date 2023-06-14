import java.util.ArrayList;
import java.util.List;
import org.junit.Test;
public class z1 {
    public static ArrayList<String> filter_list_of_str(String[] l, String s) {// returns a list of strings without the string s
        var result = new ArrayList<String>();
        if (s == null) {
            throw new IllegalArgumentException("s is null");
        }
        else if (l == null) {
            throw new IllegalArgumentException("l is null");
        }
        for (int i = 0; i < l.length; i++) {
            if (l[i] != s) {
                result.add(l[i]);
            }
        }
        return result;
    }
    @Test
    public void test_filter_list_of_str() {
        String[] l = {"a", "b", "c", "d", "e"};
        String s = "c";
        var result = filter_list_of_str(l, s);
        assert result.size() == 4;
        assert result.get(0) == "a";
        assert result.get(1) == "b";
        assert result.get(2) == "d";
        assert result.get(3) == "e";
    }
    @Test(expected = IllegalArgumentException.class)
    public void null_test_filter_list_of_string() {
        String[] l = {"a", "b", "c", "d", "e"};
        String s = null;
        var result = filter_list_of_str(l, s);
        assert result.size() == 5;
        assert result.get(0) == "a";
        assert result.get(1) == "b";
        assert result.get(2) == "c";
        assert result.get(3) == "d";
        assert result.get(4) == "e";
    }
    @Test(expected = IllegalArgumentException.class)
    public void null_test_filter_list_of_string2() {
        String[] l = null;
        String s = "c";
        var result = filter_list_of_str(l, s);
        assert result.size() == 5;
        assert result.get(0) == "a";
        assert result.get(1) == "b";
        assert result.get(2) == "c";
        assert result.get(3) == "d";
        assert result.get(4) == "e";
    }
    
    @Test
    public void test_filter_list_with_null()
    {
        String[] l = {"a", null, "c", "d", "e"};
        String s = "d";
        var result = filter_list_of_str(l, s);
        assert result.size() == 4;
        assert result.get(0) == "a";
        assert result.get(1) == null;
        assert result.get(2) == "c";
        assert result.get(3) == "e";
    }
}
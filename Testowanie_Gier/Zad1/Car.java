import java.util.HashMap;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
public class Car {
    int id;
    HashMap<String, Long> yearMillage;
    Long findMileageBetweenYears(Long startYear, Long endYear){
        Long sum = 0L;
        for (Long year = startYear; year <= endYear; year++){
            sum += yearMillage.get(year.toString());
        }
        return sum;
    }
}

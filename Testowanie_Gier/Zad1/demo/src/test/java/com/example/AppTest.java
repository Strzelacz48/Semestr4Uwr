package com.example;

import static org.junit.Assert.assertTrue;

import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;
import static org.mockito.Mockito.*;

import java.util.HashMap;
/**
 * Unit test for simple App.
 */

public class AppTest 
{
    CarDao carDao = Mockito.mock(CarDao.class);
    Car car = null;
    /**
     * Rigorous Test :-)
     */
    @Before
    public void setup(){
        car = new Car(1, new HashMap<String, Long>(), carDao);
    }
    @Test
    public void shouldAnswerWithTrue()
    {
        when(carDao.findMileageBetweenYears(car, 2000L, 2002L)).thenReturn(1000L);
        Long mileage = car.findMileageBetweenYears(2000L, 2002L);
        assertTrue( mileage == 1000L );
        assertTrue( true );
    }
}

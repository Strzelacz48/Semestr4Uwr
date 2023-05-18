package com.example;

import static org.junit.Assert.assertTrue;

import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;
import static org.mockito.Mockito.*;
import org.reldb.dbLogger.*;
import java.util.HashMap;
/**
 * Unit test for simple App.
 */

public class AppTest 
{
    // var db = new SQLiteDatabase("mylogs.sqlite");
    GenericDao genericDao = Mockito.mock(GenericDao.class);
    Session session = null;
    /**
     * Rigorous Test :-)
     */
    @Before
    public void setup(){
    }
    @Test
    public void shouldAnswerWithTrue()
    {
        Session session = new Session(genericDao);
        Student student = new Student(1);
        when(genericDao.save(any(Student.class))).thenReturn(true);
        Boolean result = session.open(student);
        assertTrue( result == true );
        assertTrue( true );
    }
    @Test
    public void shouldAnswerWithTrue2()
    {
        Session session = new Session(genericDao);
        Student student = new Student(1);
        when(genericDao.save(any(Student.class))).thenReturn(false);
        Boolean result = session.open(student);
        assertTrue( result == true );
        assertTrue( true );
    }
}

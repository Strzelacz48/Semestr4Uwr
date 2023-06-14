//import daty.java;
import java.util.ArrayList;
import java.util.Date;
import java.text.*;
import java.time.Instant;
import java.time.LocalDate;
import java.text.ParseException;
import org.junit.Test;

public class z2 {
    public static ArrayList<daty> kalendarz; // = new daty[100];
    public static void main(String[] args) {
        System.out.println("Hello World!");
    }

    public static void add_event(daty new_event) throws ParseException
    {
        
        if (new_event == null)
        {
            throw new IllegalArgumentException("new_event is null");
        }
        else if(new_event.name == null)
        {
            throw new IllegalArgumentException("new_event.name is null");
        }
        else if(new_event.start_date == null)
        {
            throw new IllegalArgumentException("new_event.start_date is null");
        }
        else if(new_event.end_date == null)
        {
            throw new IllegalArgumentException("new_event.end_date is null");
        }

        if(new_event.start_date.compareTo(new_event.end_date) > 0)
        {
            throw new IllegalArgumentException("new_event.start_date is after new_event.end_date");
        }

        for (int i = 0; i < kalendarz.size(); i++)
        {
            //==========================================================================

            SimpleDateFormat sdformat = new SimpleDateFormat("yyyy-MM-dd");
      
            //==========================================================================
            if (kalendarz.get(i).name == new_event.name)
            {
                throw new IllegalArgumentException("Event already exists");
            }
            Date d1 = sdformat.parse(kalendarz.get(i).start_date);
            Date d2 = sdformat.parse(kalendarz.get(i).end_date);
            Date d3 = sdformat.parse(new_event.start_date);
            Date d4 = sdformat.parse(new_event.end_date);

            if( (d1.compareTo(d3) <= 0 && 
            d2.compareTo(d3) > 0 )||( 
            d1.compareTo(d4) > 0 &&
            d2.compareTo(d4) <= 0) ||
            (d1.compareTo(d3) >= 0 &&
            d2.compareTo(d4) <= 0) )
            {
                throw new IllegalArgumentException("Event time taken");
            }
        }
        kalendarz.add(new_event);
        //kalendarz.add(new daty(event_name, event_time));
    }
    public static void delete_event(String event_name) throws ParseException
    {
        if (event_name == null)
        {
            throw new IllegalArgumentException("event_name is null");
        }
        for (int i = 0; i < kalendarz.size(); i++)
        {
            if (kalendarz.get(i).name == event_name)
            {
                kalendarz.remove(i);
            }
        }
    }
    public static void update_event(String event_name, String new_start_time, String new_end_time) throws ParseException
    {
        if(event_name == null)
        {
            throw new IllegalArgumentException("event_name is null");
        }
        else if(new_start_time == null)
        {
            throw new IllegalArgumentException("new_start_time is null");
        }
        else if(new_end_time == null)
        {
            throw new IllegalArgumentException("new_end_time is null");
        }

        if(new_start_time.compareTo(new_end_time) > 0)
        {
            throw new IllegalArgumentException("new_start_time is after new_end_time");
        }

        daty old_event = null;
        for (int i = 0; i < kalendarz.size(); i++)
        {
            if (kalendarz.get(i).name == event_name)
            {
                old_event = kalendarz.get(i);
                break;
            }
        }
        delete_event(event_name);
        try{
            add_event(new daty(event_name, new_start_time, new_end_time));
        }
        catch(IllegalArgumentException e)
        {
            add_event(old_event);
            throw new IllegalArgumentException("Event time taken");
        }
    }
    @Test
    public void test1() throws ParseException
    {
        kalendarz = new ArrayList<daty>();
        add_event(new daty("event1", "2020-01-01", "2020-01-02"));
        add_event(new daty("event2", "2020-01-03", "2020-01-04"));
        add_event(new daty("event3", "2020-01-05", "2020-01-06"));
        add_event(new daty("event4", "2020-01-07", "2020-01-08"));
        add_event(new daty("event5", "2020-01-09", "2020-01-10"));
        add_event(new daty("event6", "2020-01-11", "2020-01-12"));
        add_event(new daty("event7", "2020-01-13", "2020-01-14"));
        add_event(new daty("event8", "2020-01-15", "2020-01-16"));
        add_event(new daty("event9", "2020-01-17", "2020-01-18"));
        add_event(new daty("event10", "2020-01-19", "2020-01-20"));
        add_event(new daty("event11", "2020-01-21", "2020-01-22"));
        add_event(new daty("event12", "2020-01-23", "2020-01-24"));
        add_event(new daty("event13", "2020-01-25", "2020-01-26"));
        add_event(new daty("event14", "2020-01-27", "2020-01-28"));
        add_event(new daty("event15", "2020-01-29", "2020-01-30"));
        add_event(new daty("event16", "2020-01-31", "2020-02-01"));
        add_event(new daty("event17", "2020-02-02", "2020-02-03"));
        add_event(new daty("event18", "2020-02-04", "2020-02-05"));

        delete_event("event1");
        update_event("event3", "2020-09-09", "2020-09-10");

        assert(kalendarz.size() == 17);
        assert(kalendarz.get(0).name == "event2");
        assert(kalendarz.get(0).start_date == "2020-01-03");
        assert(kalendarz.get(0).end_date == "2020-01-04");
        assert(kalendarz.get(1).name == "event4");
        assert(kalendarz.get(1).start_date == "2020-01-07");
        assert(kalendarz.get(1).end_date == "2020-01-08");
        assert(kalendarz.get(16).name == "event3");
        assert(kalendarz.get(16).start_date == "2020-09-09");
        assert(kalendarz.get(16).end_date == "2020-09-10");

    }
    @Test(expected = IllegalArgumentException.class) 
    public void test_add_event_null() throws ParseException
    {
        kalendarz = new ArrayList<daty>();
        add_event(null);
    }

    @Test(expected = IllegalArgumentException.class)
    public void test_add_event_bad_date() throws ParseException
    {
        kalendarz = new ArrayList<daty>();
        add_event(new daty("event1", "2020-01-01", "2019-01-02"));
    }

    @Test(expected = IllegalArgumentException.class)
    public void test_overlapping_date() throws ParseException
    {
        kalendarz = new ArrayList<daty>();
        add_event(new daty("event1", "2020-01-01", "2020-01-02"));
        add_event(new daty("event2", "2020-01-01", "2020-01-02"));
    }
    @Test
    public void test_start_new_event_on_old_end() throws ParseException
    {
        kalendarz = new ArrayList<daty>();
        add_event(new daty("event1", "2020-01-01", "2020-01-02"));
        add_event(new daty("event2", "2020-01-02", "2020-01-03"));
        assert(kalendarz.size() == 2);
    }
}

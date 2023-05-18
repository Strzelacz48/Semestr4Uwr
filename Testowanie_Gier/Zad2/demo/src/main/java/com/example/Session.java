package com.example;

public class Session {
    GenericDao genericDao;
    public Session(GenericDao genericDao)
    {
        this.genericDao = genericDao;
    }
    private Boolean start_session()
    {
        if(true)
        {
            System.out.println("started session");
            return true;
        }
        else
        {

            throw new NullPointerException("SessionOpenException");
        }
    }
    private Boolean transaction()
    {
        if(true)
        {
            System.out.println("started transaction");
            return true;
        }
        else
        {
            throw new NullPointerException("CommitOpenException");
        }
    }
    private Boolean commit()
    {
        if(true)
        {
            System.out.println("commited");
            return true;
        }
        else
        {
            return false;
        }
    }
    private Boolean end_session()
    {
        if(true)
        {
            System.out.println("ended session");
            return true;
        }
        else
        {
            return false;
        }
    }
    public Boolean open(Student student)
    {
        try{
            start_session();
        }
        catch(NullPointerException e)
        {
            System.out.println("session start failed");
            return false;
        }
        try{
            transaction(); 
        }catch(NullPointerException e){
            System.out.println("rollback");
            System.out.println("ended session");
            return false;
        }
        
        if(!genericDao.save(student))
        {
            System.out.println("rollback");
            System.out.println("ended session");
            throw new NullPointerException("CommitOpenException");
        }
        commit();
        end_session();
        return true;
    }
    
}

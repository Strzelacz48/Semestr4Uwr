package com.example;
import java.util.HashMap;

public class Car {
    int id;
    HashMap<String, Long> yearMillage;
    CarDao carDao;
    public Car(int id, HashMap<String, Long> yearMillage, CarDao carDao){
        this.id = id;
        this.yearMillage = yearMillage;
        this.carDao = carDao;
    }
    public Long findMileageBetweenYears(Long startYear, Long endYear){
        return carDao.findMileageBetweenYears(this, startYear, endYear);
    }
}

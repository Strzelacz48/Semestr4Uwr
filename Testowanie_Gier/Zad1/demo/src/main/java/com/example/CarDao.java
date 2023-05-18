package com.example;

public class CarDao {
    public Long findMileageBetweenYears(Car car, Long startYear, Long endYear){
        Long sum = 0L;
        for (Long year = startYear; year <= endYear; year++){
            sum += car.yearMillage.get(year.toString());
        }
        return sum;
    }
}

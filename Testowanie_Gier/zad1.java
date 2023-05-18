package com.vogella.junit5;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Test;

class zad1 {

    Car calculator;

    @BeforeEach                                         
    void setUp() {
        calculator = new Calculator();
    }

    @Test                                               
    @DisplayName("Simple multiplication should work")   
    void testMultiply() {
        assertEquals(20, calculator.multiply(4, 5),     
                "Regular multiplication should work");  
    }

    @RepeatedTest(5)                                    
    @DisplayName("Ensure correct handling of zero")
    void testMultiplyWithZero() {
        assertEquals(0, calculator.multiply(0, 5), "Multiple with zero should be zero");
        assertEquals(0, calculator.multiply(5, 0), "Multiple with zero should be zero");
    }
}
/*import java.util.Scanner;
import java.util.List;
import java.util.stream.Collectors;
import java.util.Arrays;

public class zad1 {
    public class dowolna{
        public List<String> funkcja1(List<String> lista, String slowo){
            return lista.stream().filter(s -> !s.contains(slowo)).collect(Collectors.toList());
        }

    } 
    public static void main(String[] args) {

        // Creates a reader instance which takes
        // input from standard input - keyboard
        List<String> supplierNames = Arrays.asList("Ala", "ma", "kota");
        dowolna d = new dowolna();
        System.out.println(d.funkcja1(supplierNames, "ma"));
        
    }
}*/
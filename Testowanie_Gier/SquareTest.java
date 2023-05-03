import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Test;

import java.util.Random;

import static org.junit.jupiter.api.Assertions.*;

class Zad1Test {
    private final Random generator = new Random();
    private double randomInput;
    private final double epsilon = 0.0000001;

    @BeforeEach
    public void setUp() {
        randomInput = generator.nextDouble() * generator.nextInt(1000);
    }

    @RepeatedTest(5)
    public void testCalculateFromSideLength() {
        Square square = new Square(randomInput, 1);
        assertAll(
                () -> assertEquals(square.getSideLength(), randomInput, epsilon),
                () -> assertEquals(square.getArea(), randomInput * randomInput, epsilon),
                () -> assertEquals(square.getDiagonalLength(), randomInput * Math.sqrt(2), epsilon)
        );
    }

    @RepeatedTest(5)
    public void testCalculateFromDiagonalLength() {
        Square square = new Square(randomInput, 2);
        assertAll(
                () -> assertEquals(square.getSideLength(), randomInput / Math.sqrt(2), epsilon),
                () -> assertEquals(square.getArea(), (randomInput / Math.sqrt(2)) * (randomInput / Math.sqrt(2)), epsilon),
                () -> assertEquals(square.getDiagonalLength(), randomInput, epsilon)
        );
    }

    @RepeatedTest(5)
    public void testCalculateFromArea() {
        Square square = new Square(randomInput, 3);
        assertAll(
                () -> assertEquals(square.getSideLength(), Math.sqrt(randomInput), epsilon),
                () -> assertEquals(square.getArea(), randomInput, epsilon),
                () -> assertEquals(square.getDiagonalLength(), Math.sqrt(randomInput) * Math.sqrt(2), epsilon)
        );
    }

    @Test
    public void testThrowingException() {
        assertThrows(IllegalArgumentException.class, () -> new Square(randomInput, -1));
    }


}
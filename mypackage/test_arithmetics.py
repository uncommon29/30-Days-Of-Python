import unittest
import sys
import os

# Add the parent directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from arithmetics import add_numbers, subtract, multiple, division, remainder, power


class TestArithmetics(unittest.TestCase):

    def test_add_numbers(self):
        """Test the add_numbers function with various inputs"""
        self.assertEqual(add_numbers(1, 2, 3), 6)
        self.assertEqual(add_numbers(5), 5)
        self.assertEqual(add_numbers(), 0)
        self.assertEqual(add_numbers(-1, -2, -3), -6)
        self.assertEqual(add_numbers(1.5, 2.5), 4.0)
        self.assertEqual(add_numbers(10, 20, 30, 40), 100)

    def test_subtract(self):
        """Test the subtract function"""
        self.assertEqual(subtract(10, 5), 5)
        self.assertEqual(subtract(5, 10), -5)
        self.assertEqual(subtract(0, 0), 0)
        self.assertEqual(subtract(-5, -3), -2)
        self.assertEqual(subtract(7.5, 2.5), 5.0)

    def test_multiple(self):
        """Test the multiple function"""
        self.assertEqual(multiple(3, 4), 12)
        self.assertEqual(multiple(0, 5), 0)
        self.assertEqual(multiple(-2, 3), -6)
        self.assertEqual(multiple(-2, -3), 6)
        self.assertEqual(multiple(2.5, 4), 10.0)

    def test_division(self):
        """Test the division function"""
        self.assertEqual(division(10, 2), 5.0)
        self.assertEqual(division(7, 2), 3.5)
        self.assertEqual(division(-10, 2), -5.0)
        self.assertEqual(division(10, -2), -5.0)
        self.assertEqual(division(0, 5), 0.0)

    def test_division_by_zero(self):
        """Test that division by zero raises an error"""
        with self.assertRaises(ZeroDivisionError):
            division(10, 0)

    def test_remainder(self):
        """Test the remainder function"""
        self.assertEqual(remainder(10, 3), 1)
        self.assertEqual(remainder(9, 3), 0)
        self.assertEqual(remainder(7, 2), 1)
        self.assertEqual(remainder(-10, 3), 2)

    def test_power(self):
        """Test the power function"""
        self.assertEqual(power(2, 3), 8)
        self.assertEqual(power(5, 0), 1)
        self.assertEqual(power(2, -1), 0.5)
        self.assertEqual(power(3, 2), 9)
        self.assertEqual(power(2.5, 2), 6.25)


if __name__ == '__main__':
    unittest.main()

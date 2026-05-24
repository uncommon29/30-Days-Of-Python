import unittest
import sys
import os

# Add the parent directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from greet import greet_person


class TestGreet(unittest.TestCase):

    def test_greet_person(self):
        """Test the greet_person function"""
        self.assertEqual(
            greet_person("John", "Doe"),
            "John Doe, welcome to 30DaysOfPython Challenge!"
        )
        self.assertEqual(
            greet_person("Asabeneh", "Yetayeh"),
            "Asabeneh Yetayeh, welcome to 30DaysOfPython Challenge!"
        )
        self.assertEqual(
            greet_person("", ""),
            " , welcome to 30DaysOfPython Challenge!"
        )
        self.assertEqual(
            greet_person("Alice", "Smith"),
            "Alice Smith, welcome to 30DaysOfPython Challenge!"
        )


if __name__ == '__main__':
    unittest.main()

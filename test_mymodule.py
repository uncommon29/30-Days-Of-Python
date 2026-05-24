import unittest
from mymodule import generate_full_name, sum_two_nums, gravity, person


class TestMyModule(unittest.TestCase):

    def test_generate_full_name(self):
        """Test the generate_full_name function"""
        self.assertEqual(generate_full_name("John", "Doe"), "John Doe")
        self.assertEqual(generate_full_name("Asabeneh", "Yetayeh"), "Asabeneh Yetayeh")
        self.assertEqual(generate_full_name("", ""), " ")
        self.assertEqual(generate_full_name("Alice", ""), "Alice ")

    def test_sum_two_nums(self):
        """Test the sum_two_nums function"""
        self.assertEqual(sum_two_nums(2, 3), 5)
        self.assertEqual(sum_two_nums(-1, 1), 0)
        self.assertEqual(sum_two_nums(0, 0), 0)
        self.assertEqual(sum_two_nums(-5, -3), -8)
        self.assertEqual(sum_two_nums(2.5, 3.5), 6.0)

    def test_gravity_constant(self):
        """Test that gravity constant is defined correctly"""
        self.assertEqual(gravity, 9.81)
        self.assertIsInstance(gravity, float)

    def test_person_dictionary(self):
        """Test the person dictionary structure"""
        self.assertIsInstance(person, dict)
        self.assertEqual(person["firstname"], "Asabeneh")
        self.assertEqual(person["age"], 250)
        self.assertEqual(person["country"], "Finland")
        self.assertEqual(person["city"], "Helsinki")
        self.assertIn("firstname", person)
        self.assertIn("age", person)
        self.assertIn("country", person)
        self.assertIn("city", person)


if __name__ == '__main__':
    unittest.main()

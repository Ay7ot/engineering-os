import unittest

from calc import add, average, divide


class TestCore(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

    def test_divide(self):
        self.assertEqual(divide(6, 3), 2)
        with self.assertRaises(ValueError):
            divide(1, 0)

    def test_average(self):
        self.assertEqual(average([2, 4, 6]), 4)
        self.assertIsNone(average([]))


if __name__ == "__main__":
    unittest.main()

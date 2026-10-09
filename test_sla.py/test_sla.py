import unittest
from sla import is_overdue

class SLATests(unittest.TestCase):
    def test_before_limit(self):
        self.assertFalse(is_overdue(119))
    def test_at_limit(self):
        self.assertFalse(is_overdue(120))
    def test_after_limit(self):
        self.assertTrue(is_overdue(121))
    def test_high_priority(self):
        self.assertFalse(is_overdue(30, "high"))
        self.assertTrue(is_overdue(31, "high"))
    def test_low_priority(self):
        self.assertFalse(is_overdue(480, "low"))
        self.assertTrue(is_overdue(481, "low"))
    def test_zero(self):
        self.assertFalse(is_overdue(0))
    def test_negative_elapsed(self):
        with self.assertRaises(ValueError):
            is_overdue(-1)
    def test_unknown_priority(self):
        with self.assertRaises(ValueError):
            is_overdue(10, "urgent")

if __name__ == "__main__":
    unittest.main()

import unittest
from datetime import datetime, timezone, timedelta
from app.send_window import allowed, choose_start

TZ = timezone(timedelta(hours=8))

class SendWindowTests(unittest.TestCase):
    def at(self, h, m, s=0):
        return datetime(2026, 10, 4, h, m, s, tzinfo=TZ)

    def test_only_inside_requested_window(self):
        self.assertFalse(allowed(self.at(11, 39, 59)))
        self.assertTrue(allowed(self.at(11, 40)))
        self.assertTrue(allowed(self.at(11, 59, 59)))
        self.assertFalse(allowed(self.at(12, 0)))

    def test_utc_is_converted_to_beijing(self):
        self.assertTrue(allowed(datetime(2026, 10, 4, 3, 40, tzinfo=timezone.utc)))

    def test_start_before_window_and_late_runner(self):
        start = choose_start(self.at(11, 20), lambda low, high: low)
        self.assertEqual(start, self.at(11, 40))
        self.assertEqual(choose_start(self.at(11, 50), lambda low, high: low), self.at(11, 50))
        self.assertIsNone(choose_start(self.at(12, 0), lambda low, high: low))

    def test_latest_random_start_stays_before_noon(self):
        start = choose_start(self.at(11, 20), lambda low, high: high)
        self.assertTrue(allowed(start))
        self.assertLess(start, self.at(12, 0))

if __name__ == '__main__':
    unittest.main()

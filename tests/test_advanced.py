# -*- coding: utf-8 -*-

from .context import next_notifier

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        self.assertIsNone(next_notifier.hmm())


if __name__ == '__main__':
    unittest.main()

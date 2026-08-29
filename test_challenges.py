#!/usr/bin/env python3
"""
Unit tests for data structures and algorithmic challenges.
"""

import unittest
from challenges.solutions import max_subarray_sum, merge_k_sorted_lists, lru_cache_simulation


class TestChallenges(unittest.TestCase):
    def test_max_subarray(self):
        self.assertEqual(max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]), 6)
        self.assertEqual(max_subarray_sum([1]), 1)
        self.assertEqual(max_subarray_sum([5, 4, -1, 7, 8]), 23)

    def test_merge_k_sorted_lists(self):
        self.assertEqual(merge_k_sorted_lists([[1, 4, 5], [1, 3, 4], [2, 6]]), [1, 1, 2, 3, 4, 4, 5, 6])
        self.assertEqual(merge_k_sorted_lists([]), [])
        self.assertEqual(merge_k_sorted_lists([[]]), [])

    def test_lru_cache(self):
        ops = [("put", 1, 1), ("put", 2, 2), ("get", 1, 0), ("put", 3, 3), ("get", 2, 0)]
        res = lru_cache_simulation(2, ops)
        self.assertEqual(res, [None, None, 1, None, -1])


if __name__ == "__main__":
    unittest.main()

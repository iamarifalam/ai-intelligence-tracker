#!/usr/bin/env python3
"""
Algorithmic challenges and performance-optimized solutions in Python.
"""

from typing import List, Optional, Tuple


class ListNode:
    def __init__(self, val: int = 0, next: Optional['ListNode'] = None):
        self.val = val
        self.next = next


def lru_cache_simulation(capacity: int, operations: List[Tuple[str, int, int]]) -> List[Optional[int]]:
    from collections import OrderedDict
    cache = OrderedDict()
    results = []
    
    for op, key, val in operations:
        if op == "put":
            if key in cache:
                cache.move_to_end(key)
            cache[key] = val
            if len(cache) > capacity:
                cache.popitem(last=False)
            results.append(None)
        elif op == "get":
            if key not in cache:
                results.append(-1)
            else:
                cache.move_to_end(key)
                results.append(cache[key])
    return results


def max_subarray_sum(nums: List[int]) -> int:
    """Kadane's Algorithm: O(N) time, O(1) space."""
    if not nums:
        return 0
    max_so_far = current_max = nums[0]
    for x in nums[1:]:
        current_max = max(x, current_max + x)
        max_so_far = max(max_so_far, current_max)
    return max_so_far


def merge_k_sorted_lists(lists: List[List[int]]) -> List[int]:
    """Min-heap merge of K sorted lists: O(N log K)."""
    import heapq
    heap = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))
            
    merged = []
    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        merged.append(val)
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))
    return merged

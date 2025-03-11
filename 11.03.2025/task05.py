"""
Given a list of integers numbers "nums".

You need to find a sub-array with length less equal to "k", with maximal sum.

The written function should return the sum of this sub-array.

Examples:
    nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3
    result = 16
"""
from typing import List


def find_maximal_subarray_sum(nums: List[int], k: int) -> int:
    if(len(nums) == 0):
        return 0
    
    max_sum = float('-inf')
    sub_array_start = 0
    current_sum = 0

    for i in range(len(nums)):
        current_sum += nums[i]
        if i - sub_array_start + 1 > k:
            current_sum -= nums[sub_array_start]
            sub_array_start += 1
        max_sum = max(max_sum, current_sum)
    return max_sum    

print(find_maximal_subarray_sum([1, 3, -1, -3, 5, 3, 6, 7], 3))
#O(n) complexity?
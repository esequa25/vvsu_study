"""
Given a cell with "it's a fib sequence" from slideshow,
    please write function "check_fib", which accepts a Sequence of integers, and
    returns if the given sequence is a Fibonacci sequence

We guarantee, that the given sequence contain >= 0 integers inside.

"""
from collections.abc import Sequence


# def check_fibonacci(data: Sequence[int]) -> bool:
#     if data[0] == 0 and data[1] == 1:

#         for index, item in enumerate(data, start=0):
            
#             if index == 0:
#                 continue
#             if index == 1:
#                 continue
            
#             if data[index] != data[index-1] + data[index-2]:
#                 return False
#             else:
#                 return True    
#     return False

def check_fibonacci(data: Sequence[int]) -> bool:
    if data[0] == 0 and data[1] == 1 and len(data) > 2:
        for i in range(2, len(data)):
            return data[i] == data[i-1] + data[i-2]
    return False

print(check_fibonacci([0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]))
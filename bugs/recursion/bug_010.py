"""
Bug Description: Merge sort missing base case
Category: recursion
Difficulty: hard
Expected Fix: Add proper base case check and fix merge logic
"""

BUGGY_CODE = '''
def merge_sort(arr):
    if len(arr) == 0:  # Should be <= 1
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
from temp_module import merge_sort

def test_normal():
    assert merge_sort([3, 1, 4, 1, 5]) == [1, 1, 3, 4, 5]

def test_empty():
    assert merge_sort([]) == []

def test_single():
    assert merge_sort([1]) == [1]

def test_sorted():
    assert merge_sort([1, 2, 3]) == [1, 2, 3]

def test_reverse():
    assert merge_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_010")
    print(f"Description: Merge sort missing base case")
    print(f"Category: recursion")
    print(f"Difficulty: hard")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)

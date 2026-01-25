"""
Bug Description: Sum list recursive without base case
Category: recursion
Difficulty: easy
Expected Fix: Add base case for empty list
"""

BUGGY_CODE = '''
def sum_list(lst):
    return lst[0] + sum_list(lst[1:])  # Missing base case for empty list
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
from temp_module import sum_list

def test_normal_list():
    assert sum_list([1, 2, 3, 4, 5]) == 15

def test_single_element():
    assert sum_list([10]) == 10

def test_empty_list():
    assert sum_list([]) == 0

def test_negative_numbers():
    assert sum_list([-1, -2, 3]) == 0

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_004")
    print(f"Description: Sum list recursive without base case")
    print(f"Category: recursion")
    print(f"Difficulty: easy")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)

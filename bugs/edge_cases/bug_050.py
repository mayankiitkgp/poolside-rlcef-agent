"""
Bug Description: Wrong comparison operator
Category: edge_cases
Difficulty: easy
Expected Fix: Use correct comparison operator (< vs <=, == vs =)
"""

BUGGY_CODE = '''
def find_max(lst):
    if not lst:
        return None
    max_val = lst[0]
    for val in lst:
        if val < max_val:  # Should be >
            max_val = val
    return max_val
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
from temp_module import find_max

def test_normal():
    assert find_max([1, 5, 3, 9, 2]) == 9

def test_single():
    assert find_max([42]) == 42

def test_empty():
    assert find_max([]) is None

def test_negative():
    assert find_max([-1, -5, -3]) == -1

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_050")
    print(f"Description: Wrong comparison operator")
    print(f"Category: edge_cases")
    print(f"Difficulty: easy")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)

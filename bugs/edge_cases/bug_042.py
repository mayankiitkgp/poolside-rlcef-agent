"""
Bug Description: Empty list index error
Category: edge_cases
Difficulty: easy
Expected Fix: Check if list is empty before accessing
"""

BUGGY_CODE = '''
def get_first(lst):
    return lst[0]  # Crashes on empty list
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
from temp_module import get_first

def test_normal():
    assert get_first([1, 2, 3]) == 1

def test_empty():
    result = get_first([])
    assert result is None

def test_single():
    assert get_first([42]) == 42

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_042")
    print(f"Description: Empty list index error")
    print(f"Category: edge_cases")
    print(f"Difficulty: easy")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)

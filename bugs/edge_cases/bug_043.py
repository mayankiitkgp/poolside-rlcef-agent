"""
Bug Description: Negative array index unintended
Category: edge_cases
Difficulty: medium
Expected Fix: Validate index is non-negative
"""

BUGGY_CODE = '''
def get_element(arr, index):
    return arr[index]  # Negative index wraps around
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
from temp_module import get_element

def test_positive():
    assert get_element([1, 2, 3], 0) == 1

def test_negative():
    # Negative index should raise error or return None, not wrap
    try:
        result = get_element([1, 2, 3], -1)
        assert result is None, "Should not return wrapped element"
    except IndexError:
        pass

def test_out_of_range():
    try:
        get_element([1, 2, 3], 10)
        assert False
    except IndexError:
        pass

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_043")
    print(f"Description: Negative array index unintended")
    print(f"Category: edge_cases")
    print(f"Difficulty: medium")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)

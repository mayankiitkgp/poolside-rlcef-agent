"""
Bug Description: Float precision error
Category: edge_cases
Difficulty: medium
Expected Fix: Use decimal module or approximate comparison
"""

BUGGY_CODE = '''
def sum_floats(numbers):
    return sum(numbers)  # Float precision issues

def check_equal(a, b):
    return a == b  # Direct comparison fails for floats
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
from temp_module import sum_floats, check_equal

def test_sum():
    result = sum_floats([0.1, 0.2])
    assert check_equal(result, 0.3)

def test_precision():
    result = sum_floats([0.1] * 10)
    assert check_equal(result, 1.0)

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_047")
    print(f"Description: Float precision error")
    print(f"Category: edge_cases")
    print(f"Difficulty: medium")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)

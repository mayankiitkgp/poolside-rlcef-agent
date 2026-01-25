"""
Bug Description: Division by zero
Category: edge_cases
Difficulty: easy
Expected Fix: Check for zero divisor before division
"""

BUGGY_CODE = '''
def safe_divide(a, b):
    return a / b  # No zero check
'''

TEST_CODE = '''
import sys
sys.path.insert(0, '.')
from temp_module import safe_divide

def test_normal():
    assert safe_divide(10, 2) == 5.0

def test_zero():
    result = safe_divide(10, 0)
    assert result is None or result == float('inf')

def test_negative():
    assert safe_divide(-10, 2) == -5.0

'''

if __name__ == "__main__":
    print(f"Bug ID: bug_041")
    print(f"Description: Division by zero")
    print(f"Category: edge_cases")
    print(f"Difficulty: easy")
    print("\nBuggy Code:")
    print(BUGGY_CODE)
    print("\nTest Code:")
    print(TEST_CODE)
